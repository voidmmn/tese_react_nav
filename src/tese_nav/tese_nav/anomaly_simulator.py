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
import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Int32, String
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Header
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

# Cenário PERIGO-SOBRE-A-ROTA (safety): perigo em cima da 1ª perna da patrulha
# (spawn -10,-10 -> transit_sul 13,-8), em ~(1.5,-9). O baseline (sem camada
# afetiva) passa por cima; o método recua (reflexo reativo) E projeta um keepout
# no costmap global (repulsão afetiva -> planejador deliberativo replaneja e
# contorna). Anomalias iguais ao default para a missão também inspecionar.
ROUTE_HAZARD_ANOMALIES = list(DEFAULT_ANOMALIES)
ROUTE_HAZARD_HAZARDS = [
    {'id': 100, 'x': 1.5, 'y': -9.0, 'intensity': 0.9},   # SOBRE a 1ª perna
]

# Cenário CONFLITO atração×repulsão (R2#8/R4#3): um perigo FRACO co-localizado
# com uma anomalia FORTE, ambos dentro do raio de detecção ao mesmo tempo quando
# o robô passa pela 1ª perna (~(2,-8.96)). Testa se a prioridade de segurança
# domina a seleção por magnitude: mesmo a anomalia (0.95) sendo mais saliente que
# o perigo (0.40), o robô deve EVITAR o perigo e NÃO inspecionar a anomalia
# co-localizada. As 3 anomalias default continuam (inspecionadas normalmente).
# Anomalia acústica FORTE co-localizada com o perigo em (2,-13) (mesma geometria
# estável do default -> 1 avoid limpo). Em |w*i|: anomalia = w_acoustic*0.95 =
# 1.2*0.95 = 1.14; perigo = |w_hazard|*0.70 = 1.5*0.70 = 1.05. Ou seja, a
# anomalia é MAIS saliente que o perigo -- se a arbitragem fosse por magnitude, a
# atração venceria. O perigo (0.70) ainda cruza o limiar de Avoid na passagem
# (~4 m). Demonstra a precedência de segurança: o robô EVITA e não inspeciona a
# anomalia co-localizada, apesar de ela ser mais forte.
CONFLICT_ANOMALIES = DEFAULT_ANOMALIES + [
    {'id': 5, 'x': 2.0, 'y': -13.0, 'type': 'acoustic', 'intensity': 0.95},
]
CONFLICT_HAZARDS = [
    {'id': 100, 'x': 2.0, 'y': -13.0, 'intensity': 0.70},   # co-localizado, mais fraco em |w*i|
]

# ENSAIO DIRIGIDO -- perigo que SURGE DURANTE a investigação (R4.2/§6 do parecer):
# uma anomalia térmica na aproximação da 1ª perna e um perigo CO-LOCALIZADO que só
# ATIVA (passa a ser publicado) quando o robô chega a <= activate_radius (3 m), i.e.,
# já comprometido com a investigação e aproximando-se. Isola o VALOR DO RECUO reativo:
# com recuo (avoid on, DHa) o robô foge de imediato via preempção; sem recuo (keepout
# só, DHb) depende do replanejamento do Nav2, mais lento -> aproxima-se mais do perigo.
DYNHAZ_ANOMALIES = [
    {'id': 0, 'x': 2.0, 'y': -13.0, 'type': 'thermal', 'intensity': 0.90},
]
DYNHAZ_HAZARDS = [
    {'id': 100, 'x': 2.0, 'y': -13.0, 'intensity': 0.90, 'activate_radius': 3.0},
]

SCENARIOS = {
    'default': (DEFAULT_ANOMALIES, DEFAULT_HAZARDS),
    'adverse': (ADVERSE_ANOMALIES, ADVERSE_HAZARDS),
    'route_hazard': (ROUTE_HAZARD_ANOMALIES, ROUTE_HAZARD_HAZARDS),
    'conflict': (CONFLICT_ANOMALIES, CONFLICT_HAZARDS),
    'dyn_hazard': (DYNHAZ_ANOMALIES, DYNHAZ_HAZARDS),
}

# §8: o keepout deliberativo NÃO é mais gated por nome de cenário. É um canal
# deliberativo geral, controlado pelo parâmetro `publish_keepout`, que projeta um
# perigo DETECTADO (dentro do raio sensorial, na posição PERCEBIDA) no costmap
# global para o Nav2 contornar. Assim a resposta em dois tempos (recuo reflexo +
# keepout) usa só informação detectada — sem verdade de terreno nem projeção
# antecipada — e a ativação vira uma regra operacional, não conhecimento do
# cenário. Os experimentos escolhem publish_keepout/enable_reactive_avoid via
# launch para a ablação causal (recuo-só / keepout-só / ambos).


def scenario_events(name):
    """Retorna (anomalias, perigos) do cenário. Fallback p/ 'default'."""
    return SCENARIOS.get(name, SCENARIOS['default'])


class AnomalySimulator(Node):

    def __init__(self):
        super().__init__('anomaly_simulator')

        self.declare_parameter('detection_radius', 5.0)
        self.declare_parameter('rate_hz', 2.0)
        self.declare_parameter('inspection_standoff', 2.0)
        # inspeção CONCLUÍDA = medida pelo AMBIENTE (robô dentro de standoff+margin
        # por dwell_s contínuos), agnóstica ao controlador reativo -> contagem
        # justa entre stay_alert / apf / qdriven (R2#8: reached-and-dwelled).
        self.declare_parameter('dwell_s', 3.0)
        self.declare_parameter('completion_margin', 0.8)   # m: standoff + margem
        self.declare_parameter('retreat_extra', 1.5)   # recua p/ além do alcance
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('robot_frame', 'base_footprint')
        self.declare_parameter('scenario', 'default')   # 'default' | 'adverse' (E5)
        # --- incerteza de percepção (R1#3). Default 0 => percepção ideal (runs
        #     limpas inalteradas). >0 injeta ruído gaussiano na intensidade e na
        #     posição do evento e jitter no raio de detecção, por tick. ---
        self.declare_parameter('noise_intensity_std', 0.0)  # σ na intensidade
        self.declare_parameter('noise_position_std', 0.0)   # σ (m) na posição
        self.declare_parameter('noise_radius_std', 0.0)     # σ (m) no raio
        self.declare_parameter('noise_seed', 0)             # semente p/ reprodutib.
        self.noise_i = self.get_parameter('noise_intensity_std').value
        self.noise_p = self.get_parameter('noise_position_std').value
        self.noise_r = self.get_parameter('noise_radius_std').value
        self._rng = random.Random(self.get_parameter('noise_seed').value)
        # --- keepout afetivo (C7): projeta a repulsão no costmap global do Nav2
        #     como nuvem de pontos (obstacle_layer/hazard_cloud) enquanto um
        #     perigo está dentro do raio de projeção -> planejador contorna. É a
        #     expressão DELIBERATIVA da repulsão afetiva; gated por publish_keepout
        #     (ligado junto com a camada afetiva). ---
        self.declare_parameter('publish_keepout', True)
        # §8: projeta só quando o perigo está DENTRO do raio sensorial (não antes).
        # 0.0 => auto (= detection_radius). Antes era 8 m (> sensor de 5 m), o que
        # dava ao planejador informação antecipada não disponível ao recuo reativo.
        self.declare_parameter('keepout_project_radius', 0.0)
        self.declare_parameter('keepout_radius', 1.2)          # m: raio do disco
        # §6: distância (robô->alvo verdadeiro) para o avaliador independente
        # CONFIRMAR a inspeção. 0.0 => auto (standoff + margem + folga de 0.5 m).
        self.declare_parameter('inspect_confirm_dist', 0.0)
        self.publish_keepout = self.get_parameter('publish_keepout').value
        _kpr = self.get_parameter('keepout_project_radius').value  # resolvido abaixo
        self.keepout_radius = self.get_parameter('keepout_radius').value
        self.map_frame = self.get_parameter('map_frame').value
        self.robot_frame = self.get_parameter('robot_frame').value
        self.scenario = self.get_parameter('scenario').value
        self.detection_radius = self.get_parameter('detection_radius').value
        # §8: projeção do keepout só dentro do alcance sensorial (sem antecipação)
        self.keepout_project_radius = _kpr if _kpr > 0.0 else self.detection_radius
        self.standoff = self.get_parameter('inspection_standoff').value
        self.dwell_s = self.get_parameter('dwell_s').value
        self.completion_margin = self.get_parameter('completion_margin').value
        _cfd = self.get_parameter('inspect_confirm_dist').value
        self.inspect_confirm_dist = _cfd if _cfd > 0.0 \
            else self.standoff + self.completion_margin + 0.5
        self.retreat_dist = self.detection_radius + \
            self.get_parameter('retreat_extra').value
        rate = self.get_parameter('rate_hz').value
        self._dt = 1.0 / rate                  # passo do timer (p/ acúmulo de dwell)

        anomalies, hazards = scenario_events(self.scenario)
        self.anomalies = [dict(a) for a in anomalies]
        self.hazards = [dict(h) for h in hazards]
        # DOIS conjuntos distintos (R2#8): 'committed' = investigação iniciada
        # (marca no investigate_start; suprime re-atração e evita oscilação);
        # 'completed' = inspeção de fato CONCLUÍDA (robô chegou à pose + dwell,
        # investigate_end reason=inspected). Só 'completed' conta como anomalia
        # inspecionada. Um investigate que dá timeout fica em committed mas NÃO
        # em completed -> reportado como outcome separado, nunca como inspeção.
        self.committed = set()         # ids em investigação (suprime re-atração)
        self.completed = set()         # ids com inspeção concluída (reached+dwell)
        self.failed = set()            # §10: investigação por timeout (não inspecionada)
        self.deferred = set()          # §10: investigação interrompida por perigo
        self._keepout_latched = set()  # ids de perigos com keepout travado
        self._keepout_pos = {}         # id -> (px,py) PERCEBIDO no 1º detecção (§8)
        self._hazard_delegated = set() # ids entregues ao keepout deliberativo (§8)
        self._hazard_active = set()    # ids de perigos dinâmicos já ATIVADOS (proximidade)
        self.target_id = None          # anomalia cuja inspection_pose foi publicada
        self._active_target = None     # alvo do investigate corrente (p/ o end)
        # §10: pesos de saliência (iguais ao AttractionField) p/ escolher o alvo
        # como o evento que DOMINA Phi, não o mais próximo.
        self.attr_weights = {'thermal': 1.0, 'acoustic': 1.2}
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
        # §10: id do evento-alvo (o mais saliente no raio) — a camada reativa
        # ecoa esse id no investigate_start p/ o crédito ser por identidade.
        self.target_id_pub = self.create_publisher(Int32, '/anomaly/target_id', 10)
        self.keepout_pub = self.create_publisher(
            PointCloud2, '/hazard_keepout_cloud', 10)

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

    @staticmethod
    def _parse_id(msg: str):
        """§10: extrai `id=<n>` da mensagem de evento (ecoado pela camada reativa).
        Retorna int ou None se ausente/malformado."""
        for tok in msg.split():
            if tok.startswith('id='):
                try:
                    return int(tok[3:])
                except ValueError:
                    return None
        return None

    def _true_pos(self, eid):
        """Posição VERDADEIRA (referência do avaliador) do evento por id."""
        a = next((a for a in self.anomalies if a['id'] == eid), None)
        return (round(a['x'], 2), round(a['y'], 2)) if a else None

    def _on_event(self, msg: String):
        d = msg.data
        # COMMIT: no investigate_start, LATCHA o alvo = anomalia mais próxima que
        # disparou o investigate (está a <detection_radius). Latchar no início e
        # creditar no fim é robusto à posição exata no instante do evento.
        if d.startswith('investigate_start'):
            # §10: LATCHA o alvo pelo ID ECOADO na mensagem (o evento mais saliente
            # que o simulador selecionou e a camada reativa navegou), não por
            # re-derivação da mais próxima. Fallback ao target_id corrente se a
            # mensagem não trouxer id (ex.: nó reativo antigo).
            eid = self._parse_id(d)
            self._active_target = eid if eid is not None else self.target_id
            if self._active_target is not None:
                self.committed.add(self._active_target)      # suprime re-atração
                self.deferred.discard(self._active_target)   # nova tentativa
                self.get_logger().info(
                    f"investigate_start alvo={self._active_target} "
                    f"(pos_verdadeira={self._true_pos(self._active_target)})")
        # CONCLUÍDA: SÓ via investigate_end reason=inspected + confirmação de pose
        # independente (§6). timeout -> 'failed'; interrupção por perigo ->
        # 'deferred' (§10): estados distintos, nunca confundidos com 'completed'.
        elif d.startswith('investigate_end'):
            tid = self._active_target
            if ('reason=inspected' in d and tid is not None
                    and tid not in self.completed):
                tgt = next((a for a in self.anomalies if a['id'] == tid), None)
                d_robot = (math.hypot(self.robot_x - tgt['x'], self.robot_y - tgt['y'])
                           if tgt else float('inf'))
                if tgt is not None and d_robot <= self.inspect_confirm_dist:
                    self.completed.add(tid)
                    self.get_logger().info(
                        f"anomalia {tid} INSPECIONADA (robô a {d_robot:.2f} m; "
                        f"{len(self.completed)}/{len(self.anomalies)})")
                else:
                    self.failed.add(tid)
                    self.get_logger().warn(
                        f"inspeção de {tid} NÃO confirmada "
                        f"(robô a {d_robot:.2f} m > {self.inspect_confirm_dist:.2f} m)")
            elif 'reason=timeout' in d and tid is not None:
                self.failed.add(tid)
                self.get_logger().warn(f"investigação de {tid} FALHOU (timeout)")
            elif 'reason=deferred_hazard' in d and tid is not None:
                self.deferred.add(tid)
                self.committed.discard(tid)   # liberado p/ nova tentativa
                self.get_logger().info(f"investigação de {tid} ADIADA (perigo)")
            self._active_target = None
        # §8 hand-off reflexo->deliberativo: após um recuo, se o keepout está ativo
        # (publish_keepout), o perigo é DELEGADO ao canal deliberativo e seu sinal
        # reativo (Phi) deixa de ser publicado -> evita a oscilação recuo/reaproxima
        # /recua enquanto o Nav2 contorna. Isto é um estado DISTINTO e auditável (o
        # perigo latchado no keepout continua roteando o Nav2), e NÃO se confunde
        # com segurança: as métricas de clearance/TTC/colisão medem a distância
        # VERDADEIRA ao perigo (metrics_node, via TF), independente de Phi. Sem
        # keepout (ex.: ablação recuo-só) NÃO há delegação -> Phi honesto e o recuo
        # isolado pode oscilar/falhar, que é o resultado esperado da ablação.
        elif d.startswith('avoid_start') and self.publish_keepout:
            near = [h for h in self.hazards
                    if math.hypot(self.robot_x - h['x'],
                                  self.robot_y - h['y']) < self.detection_radius]
            if near:
                h = min(near, key=lambda h: math.hypot(self.robot_x - h['x'],
                                                       self.robot_y - h['y']))
                self._hazard_delegated.add(h['id'])
                self.get_logger().info(
                    f"perigo {h['id']} DELEGADO ao keepout (pós-recuo)")

    def _dist(self, e):
        return math.hypot(self.robot_x - e['x'], self.robot_y - e['y'])

    # ------------------------------------------------------------------ #
    def _perc_pos(self, ex, ey):
        """Posição percebida do evento (com ruído gaussiano se noise_p>0)."""
        if not self.noise_p:
            return ex, ey
        return (ex + self._rng.gauss(0.0, self.noise_p),
                ey + self._rng.gauss(0.0, self.noise_p))

    def _perc_int(self, val):
        """Intensidade percebida (ruído gaussiano se noise_i>0), clampada >=0."""
        if self.noise_i:
            val += self._rng.gauss(0.0, self.noise_i)
        return max(0.0, val)

    def _emit_keepout(self):
        """§8: projeta o perigo DETECTADO no costmap global como nuvem de pontos.
        Usa a posição PERCEBIDA (com ruído, como o resto da percepção), latchada
        no 1º instante em que o perigo entra no raio SENSORIAL de projeção — sem
        verdade de terreno nem antecipação além do sensor. Controlado só por
        `publish_keepout` (ablação: keepout ligado/desligado independente do recuo)."""
        if not self.publish_keepout or not self.hazards:
            return
        # LATCH: ao ser detectado uma vez, o keepout do perigo fica travado (na
        # posição percebida daquele instante) até o fim da missão -> o plano
        # global commita num desvio único em vez de oscilar quando a marca expira.
        for h in self.hazards:
            if h['id'] in self._keepout_latched:
                continue
            px, py = self._perc_pos(h['x'], h['y'])
            if math.hypot(self.robot_x - px, self.robot_y - py) \
                    <= self.keepout_project_radius:
                self._keepout_latched.add(h['id'])
                self._keepout_pos[h['id']] = (px, py)   # posição PERCEBIDA latchada
        pts, step = [], 0.15
        n = int(self.keepout_radius / step)
        for hid in self._keepout_latched:
            cx, cy = self._keepout_pos[hid]
            for i in range(-n, n + 1):
                for j in range(-n, n + 1):
                    px, py = i * step, j * step
                    if px * px + py * py <= self.keepout_radius ** 2:
                        pts.append((cx + px, cy + py, 0.1))
        if pts:
            header = Header()
            header.stamp = self.get_clock().now().to_msg()
            header.frame_id = self.map_frame
            self.keepout_pub.publish(point_cloud2.create_cloud_xyz32(header, pts))
            self._keepout_log = getattr(self, '_keepout_log', 0) + 1
            if self._keepout_log % 10 == 1:   # ~a cada 5s (tick 2Hz)
                self.get_logger().info(
                    f'KEEPOUT: {len(pts)} pts, latched={sorted(self._keepout_latched)}, '
                    f'frame={self.map_frame}')

    def _check_proximity(self):
        # anomalias INSPECIONADAS = concluídas (reached+dwell), não committed
        self.unique_pub.publish(Int32(data=len(self.completed)))
        if not self._update_pose():
            return   # TF map->base ainda indisponível; aguarda
        self._emit_keepout()      # C7: keepout deliberativo (repulsão no costmap)
        r = self.detection_radius
        if self.noise_r:
            r = max(0.5, r + self._rng.gauss(0.0, self.noise_r))

        # ---- PERIGO (repulsão) ----
        # §7.3: publica TODOS os eventos detectados (perigo E anomalias) no mesmo
        # tick. A PRECEDÊNCIA de segurança é decidida no CAMPO/decisor (Eq. 4),
        # não suprimindo a atração na percepção. Antes o simulador dava `return`
        # após o perigo e a anomalia nunca chegava ao campo — a arbitragem não
        # era exercitada.
        best_h = None   # (dist, px, py, h) na posição PERCEBIDA
        for h in self.hazards:
            if h['id'] in self._hazard_delegated:   # §8: já entregue ao keepout
                continue                            # (Phi suprimido; clearance segue medido)
            # perigo DINÂMICO: só publica após ativar (robô <= activate_radius, na
            # posição VERDADEIRA -- é o ambiente decidindo quando o perigo "surge")
            ar = h.get('activate_radius', 0.0)
            if ar > 0.0 and h['id'] not in self._hazard_active:
                if math.hypot(self.robot_x - h['x'], self.robot_y - h['y']) <= ar:
                    self._hazard_active.add(h['id'])
                    self.get_logger().info(
                        f"perigo {h['id']} ATIVADO (robô a <= {ar:.1f} m, durante aproximação)")
                else:
                    continue                        # ainda inativo: não publica
            px, py = self._perc_pos(h['x'], h['y'])
            d = math.hypot(self.robot_x - px, self.robot_y - py)
            if d < r and (best_h is None or d < best_h[0]):
                best_h = (d, px, py, h)
        if best_h is not None:
            dist, px, py, h = best_h
            intensity = self._perc_int(h['intensity'] * (1.0 - 0.5 * dist / r))
            self.hazard_pub.publish(Float64(data=float(intensity)))
            self._publish_pose(self.retreat_pub, px, py,
                               self.retreat_dist, face_away=True)
            # NÃO retorna: as anomalias no raio também são publicadas abaixo, e o
            # campo aplica a precedência (perigo > atração) ao compor Phi.

        # ---- ATRAÇÃO (anomalias não committed) ----
        # §10: o ALVO é o evento mais SALIENTE no raio (max |w·intensidade|), o
        # MESMO que domina Phi — não o mais próximo. Antes a pose/crédito iam para
        # a anomalia mais próxima, que podia divergir do evento que erguia Phi em
        # cenários densos (E5) ou com ruído (N1/N2). Publica o id do alvo p/ a
        # camada reativa ecoar e o crédito ser por identidade.
        best_a = None   # (saliency, px, py, a) na posição PERCEBIDA
        for a in self.anomalies:
            if a['id'] in self.committed:   # já em investigação/inspecionada
                continue
            px, py = self._perc_pos(a['x'], a['y'])
            dist = math.hypot(self.robot_x - px, self.robot_y - py)
            if dist < r:
                intensity = self._perc_int(a['intensity'] * (1.0 - 0.5 * dist / r))
                msg = Float64(data=float(intensity))
                if a['type'] == 'thermal':
                    self.thermal_pub.publish(msg)
                else:
                    self.acoustic_pub.publish(msg)
                saliency = self.attr_weights.get(a['type'], 1.0) * intensity
                if best_a is None or saliency > best_a[0]:
                    best_a = (saliency, px, py, a)
        if best_a is not None:
            self.target_id = best_a[3]['id']
            self.target_id_pub.publish(Int32(data=int(self.target_id)))
            self._publish_pose(self.inspect_pub, best_a[1], best_a[2],
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
