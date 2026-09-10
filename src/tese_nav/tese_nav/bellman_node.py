"""
Bellman Atratora Node — Tese de Doutorado
==========================================

Implementa Q(s,a) com termo atrativo Phi(s,a):

    Q(s,a) <- Q(s,a) + alpha[r + gamma max_a' Q(s',a') - Q(s,a)] + eta*Phi(s,a)

Responsabilidades:
  - Assina as fontes de anomalia (/anomaly/thermal, /anomaly/acoustic, /hazard).
  - Mantém o campo atrator Phi com decaimento temporal.
  - Mantém a tabela Q (atualizada a cada passo de odometria).
  - Publica o nível de atração corrente em /stay_alert/attraction, consumido
    pelo stay_alert_node, e o estado de convergência em /bellman/td_error.
"""
import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Int32
from nav_msgs.msg import Odometry

from tese_nav.utils.q_table import QTable, discretize, ACTIONS
from tese_nav.utils.attraction_field import AttractionField


class BellmanNode(Node):

    def __init__(self):
        super().__init__('bellman_node')

        # ---- Hiperparâmetros (sobrescrevíveis via bellman_params.yaml) ---- #
        self.declare_parameter('alpha', 0.1)
        self.declare_parameter('gamma', 0.95)
        self.declare_parameter('eta', 0.5)
        self.declare_parameter('cell_size', 1.0)
        self.declare_parameter('deviation_threshold', 0.6)
        self.declare_parameter('reward_progress', 1.0)

        self.alpha = self.get_parameter('alpha').value
        self.gamma = self.get_parameter('gamma').value
        self.eta = self.get_parameter('eta').value
        self.cell_size = self.get_parameter('cell_size').value
        self.deviation_threshold = self.get_parameter('deviation_threshold').value
        self.reward_progress = self.get_parameter('reward_progress').value

        self.q = QTable(alpha=self.alpha, gamma=self.gamma)
        self.field = AttractionField()

        # ---- Estado de navegação ---- #
        self.x = 0.0
        self.y = 0.0
        self._yaw = 0.0
        self._move_eps = 0.01     # m: abaixo disso, ação executada = 'stop'
        self._turn_eps = 0.05     # rad: acima disso, ação = 'left'/'right'
        self.prev_state = None
        self.prev_action = 'forward'
        self.route_deviations = 0
        self._was_above = False   # para contar desvios por borda de subida

        # ---- I/O ---- #
        self.create_subscription(Float64, '/anomaly/thermal', self._on_thermal, 10)
        self.create_subscription(Float64, '/anomaly/acoustic', self._on_acoustic, 10)
        self.create_subscription(Float64, '/hazard', self._on_hazard, 10)
        self.create_subscription(Odometry, '/odom', self._on_odom, 10)

        self.attraction_pub = self.create_publisher(Float64, '/stay_alert/attraction', 10)
        self.td_pub = self.create_publisher(Float64, '/bellman/td_error', 10)
        # resíduo COMPLETO |alpha*td + eta*Phi| (inclui o termo afetivo) — é o
        # que atesta estabilidade do update perturbado (R1#4/R2#4)
        self.residual_pub = self.create_publisher(Float64, '/bellman/update_residual', 10)
        self.dev_pub = self.create_publisher(Int32, '/bellman/route_deviations', 10)

        # decaimento + publicação periódica
        self.create_timer(self.field.decay_period, self._tick)

        self.get_logger().info(
            f'bellman_node iniciado | alpha={self.alpha} gamma={self.gamma} '
            f'eta={self.eta} limiar_desvio={self.deviation_threshold}')

    # ------------------------------------------------------------------ #
    def _on_thermal(self, msg: Float64):
        self.field.observe('thermal', msg.data)

    def _on_acoustic(self, msg: Float64):
        self.field.observe('acoustic', msg.data)

    def _on_hazard(self, msg: Float64):
        self.field.observe('hazard', msg.data)

    # ------------------------------------------------------------------ #
    def _on_odom(self, msg: Odometry):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                         1.0 - 2.0 * (q.y * q.y + q.z * q.z))

        phi = self.field.value
        state = discretize(x, y, abs(phi), cell_size=self.cell_size)

        if self.prev_state is not None:
            # §11: a ação atualizada é a EFETIVAMENTE EXECUTADA (inferida do
            # movimento real via odometria), não a greedy da tabela. Q-learning é
            # off-policy, mas o par (s,a) atualizado deve refletir a ação que
            # produziu a transição — senão a tabela não é interpretável como valor
            # das ações forward/left/right/stop.
            action = self._executed_action(x, y, yaw)
            # recompensa: apenas progresso de missão. O sinal afetivo Phi entra
            # UMA única vez, pelo termo externo eta*Phi no update (antes aparecia
            # também em max(phi,0) no reward -> dupla contagem). Manter Phi só em
            # eta*Phi torna atração/repulsão simétricas e a distinção frente ao
            # reward shaping defensável.
            reward = self.reward_progress
            self.q.update(self.prev_state, action, reward,
                          state, phi=phi, eta=self.eta)
            self.prev_action = action

        self.prev_state = state
        self.x, self.y, self._yaw = x, y, yaw

    def _executed_action(self, x, y, yaw):
        """§11: ação discreta inferida do deslocamento real desde a última odom."""
        dist = math.hypot(x - self.x, y - self.y)
        dyaw = math.atan2(math.sin(yaw - self._yaw), math.cos(yaw - self._yaw))
        # 'stop' só quando NÃO há translação NEM rotação (senão uma rotação pura,
        # dist~0 mas |dyaw| grande, era erroneamente classificada como 'stop')
        if dist < self._move_eps and abs(dyaw) < self._turn_eps:
            return 'stop'
        if abs(dyaw) > self._turn_eps:
            return 'left' if dyaw > 0 else 'right'
        return 'forward'

    # ------------------------------------------------------------------ #
    def _tick(self):
        phi = self.field.step_decay()

        self.attraction_pub.publish(Float64(data=float(phi)))

        # conta um desvio por EVENTO (transição abaixo->acima do limiar),
        # não a cada tick enquanto Phi permanece alto
        above = abs(phi) >= self.deviation_threshold
        if above and not self._was_above:
            self.route_deviations += 1
        self._was_above = above
        self.dev_pub.publish(Int32(data=self.route_deviations))

        # ler o resíduo completo ANTES do proxy (mean_abs_td reseta a janela
        # compartilhada por ambos)
        self.residual_pub.publish(Float64(data=float(self.q.mean_abs_full())))
        self.td_pub.publish(Float64(data=float(self.q.mean_abs_td())))

        if abs(phi) > 1e-3:
            self.get_logger().info(
                f'Phi={phi:+.3f} | Q-entries={self.q.size()} '
                f'| desvios={self.route_deviations}')


def main(args=None):
    rclpy.init(args=args)
    node = BellmanNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
