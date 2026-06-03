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
from geometry_msgs.msg import PoseStamped
from tf2_ros import Buffer, TransformListener, TransformException


# anomalias de ATRAÇÃO (id, x, y, tipo, intensidade) — coerentes com subestacao.sdf
DEFAULT_ANOMALIES = [
    {'id': 0, 'x': 10.0, 'y': 10.0, 'type': 'thermal', 'intensity': 0.85},
    {'id': 1, 'x': 0.0, 'y': 15.0, 'type': 'thermal', 'intensity': 0.91},
    {'id': 2, 'x': -5.0, 'y': 5.0, 'type': 'acoustic', 'intensity': 0.72},
]

# zonas de PERIGO (repulsão), persistentes. Posicionado ao LADO da 1ª perna
# (spawn -10,-10 -> transit_sul 13,-8), com o destino ALÉM dele (a leste): o
# robô passa a ~3 m, o recuo radial o empurra para o norte e ele segue a leste
# sem reentrar na zona -> UM recuo limpo (vs oscilação quando o perigo fica ao
# lado de uma perna cujo objetivo está "atrás" da zona).
DEFAULT_HAZARDS = [
    {'id': 100, 'x': 2.0, 'y': -13.0, 'intensity': 0.9},
]

# Cenário ADVERSO (E5): mesma rota, mas anomalias mais DENSAS. Clusters (2 perto
# do transformador, 2 perto do disjuntor) fazem múltiplas entrarem no raio ao
# mesmo tempo -> testa a arbitragem (qual investigar primeiro) e o
# visitado-uma-vez sob carga (5 anomalias vs 3 do default). Mantém o MESMO
# perigo do default (recuo único limpo): um 2º perigo na rota travaria o robô
# (objetivo "atrás" da zona -> AVOID infinito), então o eixo "adverso" aqui é a
# densidade de anomalias, não de perigos.
ADVERSE_ANOMALIES = [
    {'id': 0, 'x': 10.0, 'y': 10.0, 'type': 'thermal', 'intensity': 0.85},
    {'id': 1, 'x': 7.0, 'y': 8.0, 'type': 'acoustic', 'intensity': 0.78},   # cluster transformador
    {'id': 2, 'x': 0.0, 'y': 15.0, 'type': 'thermal', 'intensity': 0.91},
    {'id': 3, 'x': -5.0, 'y': 5.0, 'type': 'acoustic', 'intensity': 0.72},
    {'id': 4, 'x': -8.0, 'y': 8.0, 'type': 'thermal', 'intensity': 0.80},   # cluster disjuntor
]
ADVERSE_HAZARDS = [
    {'id': 100, 'x': 2.0, 'y': -13.0, 'intensity': 0.9},
]

SCENARIOS = {
    'default': (DEFAULT_ANOMALIES, DEFAULT_HAZARDS),
    'adverse': (ADVERSE_ANOMALIES, ADVERSE_HAZARDS),
}


def scenario_events(name):
    """Retorna (anomalias, perigos) do cenário. Fallback p/ 'default'."""
    return SCENARIOS.get(name, SCENARIOS['default'])


class AnomalySimulator(Node):

    def __init__(self):
        super().__init__('anomaly_simulator')

        self.declare_parameter('detection_radius', 5.0)
        self.declare_parameter('rate_hz', 2.0)
        self.declare_parameter('inspection_standoff', 2.0)
        self.declare_parameter('retreat_extra', 1.5)   # recua p/ além do alcance
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('robot_frame', 'base_footprint')
        self.declare_parameter('scenario', 'default')   # 'default' | 'adverse' (E5)
        self.map_frame = self.get_parameter('map_frame').value
        self.robot_frame = self.get_parameter('robot_frame').value
        self.scenario = self.get_parameter('scenario').value
        self.detection_radius = self.get_parameter('detection_radius').value
        self.standoff = self.get_parameter('inspection_standoff').value
        self.retreat_dist = self.detection_radius + \
            self.get_parameter('retreat_extra').value
        rate = self.get_parameter('rate_hz').value

        anomalies, hazards = scenario_events(self.scenario)
        self.anomalies = [dict(a) for a in anomalies]
        self.hazards = [dict(h) for h in hazards]
        self.visited = set()           # ids de anomalias já inspecionadas
        self.target_id = None          # anomalia cuja inspection_pose foi publicada
        self.robot_x = 0.0
        self.robot_y = 0.0
        self.have_pose = False

        # Pose do robô no frame MAP (via TF). NÃO usar /odom: o odom começa em
        # zero no ponto de spawn (-10,-10), ficando deslocado do frame map/world
        # onde as anomalias são definidas. TF map->base_footprint dá a pose
        # correta no mesmo frame dos eventos.
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.thermal_pub = self.create_publisher(Float64, '/anomaly/thermal', 10)
        self.acoustic_pub = self.create_publisher(Float64, '/anomaly/acoustic', 10)
        self.hazard_pub = self.create_publisher(Float64, '/hazard', 10)
        self.inspect_pub = self.create_publisher(
            PoseStamped, '/anomaly/inspection_pose', 10)
        self.retreat_pub = self.create_publisher(
            PoseStamped, '/hazard/retreat_pose', 10)
        self.unique_pub = self.create_publisher(Int32, '/anomaly/unique_detected', 10)

        # marca anomalia como visitada quando a investigação começa
        self.create_subscription(String, '/stay_alert/event', self._on_event, 10)
        self.create_timer(1.0 / rate, self._check_proximity)

        self.get_logger().info(
            f'anomaly_simulator [{self.scenario}]: {len(self.anomalies)} anomalias '
            f'+ {len(self.hazards)} perigos | alcance={self.detection_radius}m')

    # ------------------------------------------------------------------ #
    def _update_pose(self) -> bool:
        """Atualiza a pose do robô no frame map via TF. Retorna False se a
        transformada ainda não está disponível."""
        try:
            t = self.tf_buffer.lookup_transform(
                self.map_frame, self.robot_frame, rclpy.time.Time())
        except TransformException:
            return False
        self.robot_x = t.transform.translation.x
        self.robot_y = t.transform.translation.y
        self.have_pose = True
        return True

    def _on_event(self, msg: String):
        # marca a anomalia-alvo como visitada assim que a investigação COMEÇA
        # (commit). Isso impede que a MESMA anomalia volte a atrair enquanto o
        # robô ainda está no seu raio (waypoint colado nela) ou ao cruzar o
        # "vale" de Φ entre duas anomalias — eliminando a oscilação
        # PATROL<->INVESTIGATE. target_id == a anomalia cuja inspection_pose foi
        # a última publicada (mesma que o stay_alert latchou como destino).
        if msg.data.startswith('investigate_start'):
            if self.target_id is not None and self.target_id not in self.visited:
                a = next((x for x in self.anomalies
                          if x['id'] == self.target_id), None)
                if a is not None:
                    self.visited.add(a['id'])
                    self.get_logger().info(
                        f"anomalia {a['id']} ({a['type']}) em investigação "
                        f"-> visitada ({len(self.visited)}/{len(self.anomalies)})")

    def _dist(self, e):
        return math.hypot(self.robot_x - e['x'], self.robot_y - e['y'])

    # ------------------------------------------------------------------ #
    def _check_proximity(self):
        self.unique_pub.publish(Int32(data=len(self.visited)))
        if not self._update_pose():
            return   # TF map->base ainda indisponível; aguarda
        r = self.detection_radius

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
            self.target_id = nearest[1]['id']
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
