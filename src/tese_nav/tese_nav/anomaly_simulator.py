"""
Anomaly Simulator Node.
=======================

Abstrai a SAÍDA da cadeia sensor+percepção como EVENTOS (modalidade +
intensidade + posição), sem simular os sensores crus. Dois tipos:

  ATRAÇÃO (Φ>0): pontos quentes (térmica) / descargas (acústica) — o robô deve
    se APROXIMAR e investigar. Cada anomalia é inspecionada UMA VEZ: após o
    stay_alert sinalizar investigate_end, ela é marcada como visitada e para de
    atrair (evita oscilação e dá a contagem de anomalias únicas).

  REPULSÃO (Φ<0): zonas de perigo (ex.: arco elétrico / vazamento de SF6) — o
    robô deve se AFASTAR. Persistentes: sempre repelem quando sensoriadas.

Publica, quando dentro do alcance sensorial (detection_radius):
  /anomaly/thermal | /anomaly/acoustic (Float64)   intensidade da atração
  /hazard (Float64)                                  intensidade do perigo
  /anomaly/inspection_pose (PoseStamped, map)        para onde APROXIMAR
  /hazard/retreat_pose (PoseStamped, map)            para onde RECUAR
  /anomaly/unique_detected (Int32)                   nº de anomalias já visitadas
"""
import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Int32, String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped


# anomalias de ATRAÇÃO (id, x, y, tipo, intensidade) — coerentes com subestacao.sdf
DEFAULT_ANOMALIES = [
    {'id': 0, 'x': 10.0, 'y': 10.0, 'type': 'thermal', 'intensity': 0.85},
    {'id': 1, 'x': 0.0, 'y': 15.0, 'type': 'thermal', 'intensity': 0.91},
    {'id': 2, 'x': -5.0, 'y': 5.0, 'type': 'acoustic', 'intensity': 0.72},
]

# zonas de PERIGO (repulsão), persistentes — ao lado da rota de transição
DEFAULT_HAZARDS = [
    {'id': 100, 'x': 16.0, 'y': 0.0, 'intensity': 0.9},
]


class AnomalySimulator(Node):

    def __init__(self):
        super().__init__('anomaly_simulator')

        self.declare_parameter('detection_radius', 5.0)
        self.declare_parameter('rate_hz', 2.0)
        self.declare_parameter('inspection_standoff', 2.0)
        self.declare_parameter('retreat_extra', 1.5)   # recua p/ além do alcance
        self.detection_radius = self.get_parameter('detection_radius').value
        self.standoff = self.get_parameter('inspection_standoff').value
        self.retreat_dist = self.detection_radius + \
            self.get_parameter('retreat_extra').value
        rate = self.get_parameter('rate_hz').value

        self.anomalies = [dict(a) for a in DEFAULT_ANOMALIES]
        self.hazards = [dict(h) for h in DEFAULT_HAZARDS]
        self.visited = set()           # ids de anomalias já inspecionadas
        self.robot_x = 0.0
        self.robot_y = 0.0

        self.thermal_pub = self.create_publisher(Float64, '/anomaly/thermal', 10)
        self.acoustic_pub = self.create_publisher(Float64, '/anomaly/acoustic', 10)
        self.hazard_pub = self.create_publisher(Float64, '/hazard', 10)
        self.inspect_pub = self.create_publisher(
            PoseStamped, '/anomaly/inspection_pose', 10)
        self.retreat_pub = self.create_publisher(
            PoseStamped, '/hazard/retreat_pose', 10)
        self.unique_pub = self.create_publisher(Int32, '/anomaly/unique_detected', 10)

        self.create_subscription(Odometry, '/odom', self._on_odom, 10)
        # marca anomalia como visitada quando a investigação termina
        self.create_subscription(String, '/stay_alert/event', self._on_event, 10)
        self.create_timer(1.0 / rate, self._check_proximity)

        self.get_logger().info(
            f'anomaly_simulator: {len(self.anomalies)} anomalias + '
            f'{len(self.hazards)} perigos | alcance={self.detection_radius}m')

    # ------------------------------------------------------------------ #
    def _on_odom(self, msg: Odometry):
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y

    def _on_event(self, msg: String):
        # ao terminar uma investigação, marca a anomalia de atração mais próxima
        # (não visitada, dentro do alcance) como inspecionada
        if msg.data.startswith('investigate_end'):
            cand = [a for a in self.anomalies if a['id'] not in self.visited
                    and self._dist(a) < self.detection_radius]
            if cand:
                nearest = min(cand, key=self._dist)
                self.visited.add(nearest['id'])
                self.get_logger().info(
                    f"anomalia {nearest['id']} ({nearest['type']}) inspecionada "
                    f"-> visitada ({len(self.visited)}/{len(self.anomalies)})")

    def _dist(self, e):
        return math.hypot(self.robot_x - e['x'], self.robot_y - e['y'])

    # ------------------------------------------------------------------ #
    def _check_proximity(self):
        r = self.detection_radius
        self.unique_pub.publish(Int32(data=len(self.visited)))

        # ---- PERIGO (repulsão) tem prioridade: segurança antes de inspeção ----
        haz = [(self._dist(h), h) for h in self.hazards if self._dist(h) < r]
        if haz:
            dist, h = min(haz, key=lambda t: t[0])
            intensity = h['intensity'] * (1.0 - 0.5 * dist / r)
            self.hazard_pub.publish(Float64(data=float(intensity)))
            self._publish_pose(self.retreat_pub, h['x'], h['y'],
                               self.retreat_dist, face_away=True)
            return   # perto de perigo: não investiga anomalia neste tick

        # ---- ATRAÇÃO (anomalias não visitadas) ----
        nearest = None
        for a in self.anomalies:
            if a['id'] in self.visited:
                continue
            dist = self._dist(a)
            if dist < r:
                intensity = a['intensity'] * (1.0 - 0.5 * dist / r)
                msg = Float64(data=float(intensity))
                if a['type'] == 'thermal':
                    self.thermal_pub.publish(msg)
                else:
                    self.acoustic_pub.publish(msg)
                if nearest is None or dist < nearest[0]:
                    nearest = (dist, a)
        if nearest is not None:
            self._publish_pose(self.inspect_pub, nearest[1]['x'], nearest[1]['y'],
                               self.standoff, face_away=False)

    def _publish_pose(self, pub, ex, ey, standoff, face_away):
        """Pose a `standoff` do evento, na direção do robô. face_away controla
        a orientação: False = olhando para o evento (inspeção); True = de costas
        (recuo)."""
        dx, dy = self.robot_x - ex, self.robot_y - ey
        d = math.hypot(dx, dy)
        ux, uy = (1.0, 0.0) if d < 1e-3 else (dx / d, dy / d)
        px, py = ex + ux * standoff, ey + uy * standoff
        # olhar para o evento: yaw = atan2(-uy,-ux); de costas: atan2(uy,ux)
        yaw = math.atan2(uy, ux) if face_away else math.atan2(-uy, -ux)

        ps = PoseStamped()
        ps.header.frame_id = 'map'
        ps.header.stamp = self.get_clock().now().to_msg()
        ps.pose.position.x = float(px)
        ps.pose.position.y = float(py)
        ps.pose.orientation.z = math.sin(yaw / 2.0)
        ps.pose.orientation.w = math.cos(yaw / 2.0)
        pub.publish(ps)


def main(args=None):
    rclpy.init(args=args)
    node = AnomalySimulator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
