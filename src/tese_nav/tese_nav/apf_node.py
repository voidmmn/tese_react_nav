"""
APF Node — baseline reativo de CAMPO POTENCIAL ARTIFICIAL.
==========================================================

Substitui a camada reativa Stay Alert (mesmo interface /stay_alert/*), mantendo
a MESMA patrulha Nav2 por baixo. Enquanto patrulha, deixa o Nav2 dirigir. Quando
o campo de forças (atração a anomalias + repulsão de perigos) ultrapassa um
limiar, PAUSA o Nav2 (via /stay_alert/active) e assume o /cmd_vel, dirigindo o
robô pelo vetor de força resultante — atração até a anomalia (inspeção) ou
repulsão do perigo (recuo) — com repulsão adicional de obstáculos (/scan) para
não colidir com as estruturas. É o baseline "APF clássico rodado nos mesmos
eventos" (R2.5b/R4.2): difere do Stay Alert por ser força contínua com soma
vetorial (sem commit por limiar/argmax), exibindo o comportamento próprio do APF.

Publica o MESMO protocolo do stay_alert_node para reusar métricas e contagem:
    /stay_alert/active (Bool), /stay_alert/mode (String), /stay_alert/event (String)
"""
import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from tf2_ros import Buffer, TransformListener, TransformException

from tese_nav.anomaly_simulator import scenario_events


def yaw_from_quat(z, w):
    return math.atan2(2.0 * w * z, 1.0 - 2.0 * z * z)


def ang_diff(a, b):
    d = a - b
    return math.atan2(math.sin(d), math.cos(d))


class ApfNode(Node):

    PATROL = 'PATROL'
    INVESTIGATE = 'INVESTIGATE'
    AVOID = 'AVOID'

    def __init__(self):
        super().__init__('apf_node')

        self.declare_parameter('scenario', 'default')
        self.declare_parameter('detection_radius', 5.0)
        # gains calibrados p/ o APF disparar dentro do raio de detecção como o
        # método (baseline justo): atração cruza o limiar p/ waypoints a ~4-5 m;
        # repulsão cruza no ~4.7 m de passagem do perigo beside-route.
        self.declare_parameter('force_threshold', 0.15)  # |F| p/ disparar episódio
        self.declare_parameter('exit_threshold', 0.08)
        self.declare_parameter('k_att', 1.5)             # ganho de atração
        self.declare_parameter('k_rep', 4.0)             # ganho de repulsão (perigo)
        self.declare_parameter('k_obs', 0.6)             # ganho de repulsão (/scan)
        self.declare_parameter('obs_influence', 1.2)     # m: alcance da repulsão de obstáculo
        self.declare_parameter('k_lin', 0.5)
        self.declare_parameter('k_ang', 1.5)
        self.declare_parameter('max_lin', 0.35)
        self.declare_parameter('max_ang', 1.2)
        self.declare_parameter('standoff', 1.8)          # m: distância de inspeção
        self.declare_parameter('dwell_s', 3.0)
        self.declare_parameter('max_investigation_s', 30.0)
        # refratário pós-recuo: augmentação padrão contra a oscilação conhecida do
        # APF (perna da ronda passa dentro do gatilho -> recua/reaproxima em loop).
        # Bloqueia re-AVOID por um tempo p/ o Nav2 progredir além do perigo.
        self.declare_parameter('avoid_refractory_s', 12.0)
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('robot_frame', 'base_footprint')

        g = lambda k: self.get_parameter(k).value
        self.scenario = g('scenario')
        self.detection_radius = g('detection_radius')
        self.force_threshold = g('force_threshold')
        self.exit_threshold = g('exit_threshold')
        self.k_att, self.k_rep, self.k_obs = g('k_att'), g('k_rep'), g('k_obs')
        self.obs_influence = g('obs_influence')
        self.k_lin, self.k_ang = g('k_lin'), g('k_ang')
        self.max_lin, self.max_ang = g('max_lin'), g('max_ang')
        self.standoff = g('standoff')
        self.dwell_s = g('dwell_s')
        self.max_investigation_s = g('max_investigation_s')
        self.avoid_refractory_s = g('avoid_refractory_s')
        self._avoid_until = 0.0
        self.map_frame, self.robot_frame = g('map_frame'), g('robot_frame')

        anomalies, hazards = scenario_events(self.scenario)
        self.anomalies = [dict(a) for a in anomalies]
        self.hazards = [dict(h) for h in hazards]
        self.committed = set()   # §10: alvos em investigação (era 'visited')

        self.mode = self.PATROL
        self.target = None            # anomalia-alvo do INVESTIGATE
        self._t_start = None
        self._reached_since = None
        self.scan = None              # última LaserScan (repulsão de obstáculo)

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.create_subscription(LaserScan, '/scan', self._on_scan, 10)

        self.active_pub = self.create_publisher(Bool, '/stay_alert/active', 10)
        self.mode_pub = self.create_publisher(String, '/stay_alert/mode', 10)
        self.event_pub = self.create_publisher(String, '/stay_alert/event', 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.create_timer(0.1, self._update)
        self._publish_mode()
        self.get_logger().info(
            f'apf_node [{self.scenario}] iniciado | thr={self.force_threshold} '
            f'k_att={self.k_att} k_rep={self.k_rep}')

    # ------------------------------------------------------------------ #
    def _on_scan(self, msg: LaserScan):
        self.scan = msg

    def _pose(self):
        try:
            t = self.tf_buffer.lookup_transform(
                self.map_frame, self.robot_frame, rclpy.time.Time())
        except TransformException:
            return None
        x = t.transform.translation.x
        y = t.transform.translation.y
        yaw = yaw_from_quat(t.transform.rotation.z, t.transform.rotation.w)
        return x, y, yaw

    def _attraction(self, x, y):
        """Força atrativa (soma vetorial) das anomalias não visitadas em alcance."""
        fx = fy = 0.0
        best = None
        for a in self.anomalies:
            if a['id'] in self.committed:
                continue
            dx, dy = a['x'] - x, a['y'] - y
            d = math.hypot(dx, dy)
            if d < self.detection_radius and d > 1e-3:
                mag = self.k_att * a['intensity'] / max(d, 0.5)
                fx += mag * dx / d
                fy += mag * dy / d
                if best is None or d < best[1]:
                    best = (a, d)
        return fx, fy, best

    def _repulsion(self, x, y):
        """Força repulsiva (soma vetorial) dos perigos em alcance."""
        fx = fy = 0.0
        nearest = None
        for h in self.hazards:
            dx, dy = x - h['x'], y - h['y']
            d = math.hypot(dx, dy)
            if d < self.detection_radius and d > 1e-3:
                mag = self.k_rep * h['intensity'] / (d * d)
                fx += mag * dx / d
                fy += mag * dy / d
                if nearest is None or d < nearest:
                    nearest = d
        return fx, fy, nearest

    def _obstacle_force(self, yaw):
        """Repulsão de obstáculos a partir da /scan (no frame do robô -> map)."""
        if self.scan is None:
            return 0.0, 0.0
        fx = fy = 0.0
        ang = self.scan.angle_min
        inc = self.scan.angle_increment
        for r in self.scan.ranges:
            if math.isfinite(r) and 0.05 < r < self.obs_influence:
                # ponto do obstáculo no frame do robô; repulsão na direção oposta
                mag = self.k_obs * (1.0 / r - 1.0 / self.obs_influence) / (r * r)
                world_ang = yaw + ang
                fx -= mag * math.cos(world_ang)
                fy -= mag * math.sin(world_ang)
            ang += inc
        return fx, fy

    # ------------------------------------------------------------------ #
    def _update(self):
        p = self._pose()
        if p is None:
            return
        x, y, yaw = p
        now = self.now_s()

        fa_x, fa_y, best = self._attraction(x, y)
        fr_x, fr_y, haz_d = self._repulsion(x, y)
        att_mag = math.hypot(fa_x, fa_y)
        rep_mag = math.hypot(fr_x, fr_y)

        if self.mode == self.PATROL:
            if rep_mag >= self.force_threshold and now >= self._avoid_until:
                self._enter(self.AVOID, None, now)
            elif att_mag >= self.force_threshold and best is not None:
                self._enter(self.INVESTIGATE, best[0], now)
            return

        # --- episódio reativo: assume o /cmd_vel pelo vetor de força ---
        ox, oy = self._obstacle_force(yaw)
        elapsed = now - self._t_start

        if self.mode == self.INVESTIGATE:
            fx, fy = fa_x + ox, fa_y + oy
            d_target = math.hypot(self.target['x'] - x, self.target['y'] - y) \
                if self.target else 1e9
            if d_target <= self.standoff:
                self._drive(0.0, 0.0)               # parado, observando
                if self._reached_since is None:
                    self._reached_since = now
                elif now - self._reached_since >= self.dwell_s:
                    self.committed.add(self.target['id'])
                    self._exit('inspected', elapsed)
                return
            if elapsed >= self.max_investigation_s:
                self._exit('timeout', elapsed)
                return
            self._drive_toward(fx, fy, yaw)

        elif self.mode == self.AVOID:
            fx, fy = fr_x + ox, fr_y + oy
            if rep_mag < self.exit_threshold:
                self._exit('safe', elapsed)
                return
            if elapsed >= self.max_investigation_s:
                self._exit('timeout', elapsed)
                return
            self._drive_toward(fx, fy, yaw)

    # ------------------------------------------------------------------ #
    def _drive_toward(self, fx, fy, yaw):
        mag = math.hypot(fx, fy)
        if mag < 1e-6:
            self._drive(0.0, 0.0)
            return
        desired = math.atan2(fy, fx)
        err = ang_diff(desired, yaw)
        ang = max(-self.max_ang, min(self.max_ang, self.k_ang * err))
        # avança só quando razoavelmente alinhado (reduz por cos do erro)
        lin = self.k_lin * mag * max(0.0, math.cos(err))
        lin = max(0.0, min(self.max_lin, lin))
        self._drive(lin, ang)

    def _drive(self, lin, ang):
        tw = Twist()
        tw.linear.x = float(lin)
        tw.angular.z = float(ang)
        self.cmd_pub.publish(tw)

    def _enter(self, mode, target, now):
        self.mode = mode
        self.target = target
        self._t_start = now
        self._reached_since = None
        self.active_pub.publish(Bool(data=True))    # pausa a ronda (Nav2 idle)
        self._publish_mode()
        tag = 'investigate_start' if mode == self.INVESTIGATE else 'avoid_start'
        # §10: ecoa o id do alvo (APF o conhece: seleciona da própria geometria)
        eid = target['id'] if (mode == self.INVESTIGATE and target) else -1
        self.event_pub.publish(String(data=f'{tag} id={eid} apf'))
        self.get_logger().info(f'APF -> {mode}')

    def _exit(self, reason, elapsed):
        ending = self.mode
        if ending == self.AVOID:            # refratário p/ evitar oscilação APF
            self._avoid_until = self.now_s() + self.avoid_refractory_s
        self.mode = self.PATROL
        self.target = None
        self._reached_since = None
        self._drive(0.0, 0.0)
        self.active_pub.publish(Bool(data=False))   # retoma a ronda
        self._publish_mode()
        tag = 'investigate_end' if ending == self.INVESTIGATE else 'avoid_end'
        self.event_pub.publish(String(data=f'{tag} reason={reason} dur={elapsed:.1f}'))
        self.get_logger().info(f'APF <- PATROL ({reason}, {elapsed:.1f}s)')

    def _publish_mode(self):
        self.mode_pub.publish(String(data=self.mode))

    def now_s(self):
        return self.get_clock().now().nanoseconds / 1e9


def main(args=None):
    rclpy.init(args=args)
    node = ApfNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
