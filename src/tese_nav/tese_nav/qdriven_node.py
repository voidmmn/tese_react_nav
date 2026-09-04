"""
Q-driven Node — baseline REWARD-AUGMENTED Q-LEARNING (RL comportamental).
========================================================================

Substitui a camada reativa Stay Alert (mesmo interface /stay_alert/*), mesma
patrulha Nav2 por baixo. Diferença-chave vs o método proposto: aqui a Q-table
SELECIONA a ação executada {forward,left,right,stop} (greedy) que dirige o
/cmd_vel durante o episódio reativo — é RL comportamental (Q atua), enquanto no
método a Q é passiva e o disparo é por limiar. A Q foi PRÉ-TREINADA
(train_qdriven.py, sim cinemático) com recompensa aumentada por Φ; aqui roda
greedy (ε=0). Responde ao R2.5c.

Publica o mesmo protocolo do stay_alert_node (active/mode/event) p/ reusar
métricas e a contagem de inspeção medida por proximidade do anomaly_simulator.
"""
import json
import math
import os

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from ament_index_python.packages import get_package_share_directory
from tf2_ros import Buffer, TransformListener, TransformException

from tese_nav.anomaly_simulator import scenario_events
from tese_nav.utils.qdriven_core import (
    ACTIONS, ACTION_CMD, discretize, bearing_to, wrap)


def yaw_from_quat(z, w):
    return math.atan2(2.0 * w * z, 1.0 - 2.0 * z * z)


class QDrivenNode(Node):

    PATROL = 'PATROL'
    INVESTIGATE = 'INVESTIGATE'
    AVOID = 'AVOID'

    def __init__(self):
        super().__init__('qdriven_node')

        self.declare_parameter('scenario', 'default')
        self.declare_parameter('detection_radius', 5.0)
        self.declare_parameter('standoff', 1.8)
        self.declare_parameter('safe_dist', 6.0)
        self.declare_parameter('dwell_s', 3.0)
        self.declare_parameter('max_investigation_s', 30.0)
        self.declare_parameter('avoid_refractory_s', 12.0)
        # veto de segurança por /scan: a política treinada não tem desvio de
        # obstáculo (sim de treino só tinha ponto+evento); sem isto o bang-bang
        # dirige o robô p/ dentro das estruturas e o Nav2 não replaneja de lá.
        self.declare_parameter('safety_dist', 0.7)   # m: obstáculo à frente
        self.declare_parameter('safe_cone', 0.5)     # rad: meia-abertura do cone
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('robot_frame', 'base_footprint')
        self.declare_parameter('qtable_file', '')

        g = lambda k: self.get_parameter(k).value
        self.scenario = g('scenario')
        self.detection_radius = g('detection_radius')
        self.standoff = g('standoff')
        self.safe_dist = g('safe_dist')
        self.dwell_s = g('dwell_s')
        self.max_investigation_s = g('max_investigation_s')
        self.avoid_refractory_s = g('avoid_refractory_s')
        self.safety_dist = g('safety_dist')
        self.safe_cone = g('safe_cone')
        self.scan = None
        self.map_frame, self.robot_frame = g('map_frame'), g('robot_frame')

        qfile = g('qtable_file') or os.path.join(
            get_package_share_directory('tese_nav'), 'config', 'qtable_qdriven.json')
        self.Q = self._load_q(qfile)

        anomalies, hazards = scenario_events(self.scenario)
        self.anomalies = [dict(a) for a in anomalies]
        self.hazards = [dict(h) for h in hazards]
        self.visited = set()

        self.mode = self.PATROL
        self._t_start = None
        self._reached_since = None
        self._avoid_until = 0.0

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
            f'qdriven_node [{self.scenario}] | Q={len(self.Q)} estados de {qfile}')

    def _load_q(self, path):
        with open(path) as fh:
            data = json.load(fh)
        return {tuple(int(x) for x in k.split(',')): v
                for k, v in data['q'].items()}

    def _greedy(self, state):
        qs = self.Q.get(state)
        if qs is None:
            return 'forward'      # estado não visto no treino: avança
        return ACTIONS[max(range(len(ACTIONS)), key=lambda i: qs[i])]

    def _on_scan(self, msg):
        self.scan = msg

    def _cone_min(self, lo, hi):
        """Menor alcance da /scan no setor angular [lo,hi] (rad, frame do robô)."""
        if self.scan is None:
            return float('inf')
        s = self.scan
        m = float('inf')
        ang = s.angle_min
        for r in s.ranges:
            if lo <= ang <= hi and math.isfinite(r) and r > 0.05 and r < m:
                m = r
            ang += s.angle_increment
        return m

    def _veto(self, lin, ang):
        """Segurança: se a ação avança para um obstáculo à frente, gira no lugar
        para o lado mais aberto em vez de colidir (a política não tem isto)."""
        if lin > 0.0 and self._cone_min(-self.safe_cone, self.safe_cone) < self.safety_dist:
            left = self._cone_min(self.safe_cone, 1.6)
            right = self._cone_min(-1.6, -self.safe_cone)
            return 0.0, (0.7 if left >= right else -0.7)
        return lin, ang

    # ------------------------------------------------------------------ #
    def _pose(self):
        try:
            t = self.tf_buffer.lookup_transform(
                self.map_frame, self.robot_frame, rclpy.time.Time())
        except TransformException:
            return None
        return (t.transform.translation.x, t.transform.translation.y,
                yaw_from_quat(t.transform.rotation.z, t.transform.rotation.w))

    def _nearest(self, items, x, y, skip=None):
        best = None
        for e in items:
            if skip and e['id'] in skip:
                continue
            d = math.hypot(e['x'] - x, e['y'] - y)
            if d < self.detection_radius and (best is None or d < best[1]):
                best = (e, d)
        return best

    def _update(self):
        p = self._pose()
        if p is None:
            return
        x, y, yaw = p
        now = self.now_s()

        haz = self._nearest(self.hazards, x, y)
        anom = self._nearest(self.anomalies, x, y, skip=self.visited)

        if self.mode == self.PATROL:
            if haz is not None and now >= self._avoid_until:
                self._enter(self.AVOID, haz[0], now)
            elif anom is not None:
                self._enter(self.INVESTIGATE, anom[0], now)
            return

        elapsed = now - self._t_start
        e = self.target
        d = math.hypot(e['x'] - x, e['y'] - y)
        ev_type = 'anomaly' if self.mode == self.INVESTIGATE else 'hazard'

        # terminação do episódio
        if self.mode == self.INVESTIGATE:
            if d <= self.standoff:
                self._drive(0.0, 0.0)
                if self._reached_since is None:
                    self._reached_since = now
                elif now - self._reached_since >= self.dwell_s:
                    self.visited.add(e['id'])
                    self._exit('inspected', elapsed)
                return
            if elapsed >= self.max_investigation_s:
                self._exit('timeout', elapsed)
                return
        else:  # AVOID
            if d >= self.safe_dist:
                self._exit('safe', elapsed)
                return
            if elapsed >= self.max_investigation_s:
                self._exit('timeout', elapsed)
                return

        # ação vem da Q-table greedy (RL comportamental), com veto de segurança
        bearing = wrap(bearing_to(x, y, yaw, e['x'], e['y']))
        action = self._greedy(discretize(ev_type, d, bearing))
        lin, ang = self._veto(*ACTION_CMD[action])
        self._drive(lin, ang)

    # ------------------------------------------------------------------ #
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
        self.active_pub.publish(Bool(data=True))
        self._publish_mode()
        tag = 'investigate_start' if mode == self.INVESTIGATE else 'avoid_start'
        self.event_pub.publish(String(data=f'{tag} qdriven'))
        self.get_logger().info(f'Qdriven -> {mode}')

    def _exit(self, reason, elapsed):
        ending = self.mode
        if ending == self.AVOID:
            self._avoid_until = self.now_s() + self.avoid_refractory_s
        self.mode = self.PATROL
        self.target = None
        self._reached_since = None
        self._drive(0.0, 0.0)
        self.active_pub.publish(Bool(data=False))
        self._publish_mode()
        tag = 'investigate_end' if ending == self.INVESTIGATE else 'avoid_end'
        self.event_pub.publish(String(data=f'{tag} reason={reason} dur={elapsed:.1f}'))
        self.get_logger().info(f'Qdriven <- PATROL ({reason}, {elapsed:.1f}s)')

    def _publish_mode(self):
        self.mode_pub.publish(String(data=self.mode))

    def now_s(self):
        return self.get_clock().now().nanoseconds / 1e9


def main(args=None):
    rclpy.init(args=args)
    node = QDrivenNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
