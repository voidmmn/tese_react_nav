"""
Stay Alert Node — terceiro modo de missão.
==========================================

Entre os waypoints de inspeção, o robô segue a rota planejada pelo Nav2
(modo PATROL). Quando o campo atrator Phi (publicado por bellman_node)
ultrapassa um limiar, o robô entra em modo INVESTIGATE: a missão de
waypoints é pausada e o robô investiga a anomalia por um tempo limitado;
em seguida retoma a ronda.

Desvio ATIVO: ao entrar em INVESTIGATE, o nó assume o controle da navegação
e envia o robô (via Nav2 NavigateToPose) até a pose de inspeção da anomalia
(publicada pelo anomaly_simulator em /anomaly/inspection_pose). O mission_node
pausa a ronda enquanto /stay_alert/active=True e retoma o mesmo waypoint depois.

Máquina de estados:
    PATROL  --(Phi >= enter_threshold)-->  INVESTIGATE (vai até a anomalia)
    INVESTIGATE --(chegou+dwell | tempo esgotado | Phi < exit_threshold)--> PATROL

Saídas:
    /stay_alert/active (Bool)   -> mission_node pausa/retoma waypoints
    /stay_alert/mode   (String) -> "PATROL" | "INVESTIGATE" (métricas/RViz)
    /stay_alert/event  (String) -> eventos rotulados para metrics_node
"""
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from std_msgs.msg import Float64, Bool, String
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose


class StayAlertNode(Node):

    PATROL = 'PATROL'
    INVESTIGATE = 'INVESTIGATE'   # atração (Φ>0): aproxima da anomalia
    AVOID = 'AVOID'               # repulsão (Φ<0): recua do perigo

    def __init__(self):
        super().__init__('stay_alert_node')

        self.declare_parameter('enter_threshold', 0.6)
        self.declare_parameter('exit_threshold', 0.3)
        self.declare_parameter('max_investigation_s', 15.0)
        # tempo de observação parado após chegar na pose de inspeção
        self.declare_parameter('dwell_s', 3.0)
        # C7: refratário após um recuo. Impede re-disparo imediato de AVOID
        # (recua->reaproxima->recua) enquanto o keepout no costmap faz o Nav2
        # replanejar e contornar o perigo. Dá a hand-off reflexo->deliberativo.
        self.declare_parameter('avoid_refractory_s', 8.0)

        self.enter_threshold = self.get_parameter('enter_threshold').value
        self.exit_threshold = self.get_parameter('exit_threshold').value
        self.max_investigation_s = self.get_parameter('max_investigation_s').value
        self.dwell_s = self.get_parameter('dwell_s').value
        self.avoid_refractory_s = self.get_parameter('avoid_refractory_s').value
        self._avoid_until = 0.0   # instante até o qual AVOID fica bloqueado

        self.mode = self.PATROL
        self.phi = 0.0
        self._investigate_start = None
        self.target_pose = None       # pose de inspeção (atração)
        self.retreat_pose = None      # pose de recuo (repulsão)
        self._goal_handle = None       # goal Nav2 corrente (investigação/recuo)
        self._reached_at = None        # quando chegou ao destino

        self.create_subscription(Float64, '/stay_alert/attraction', self._on_phi, 10)
        self.create_subscription(PoseStamped, '/anomaly/inspection_pose',
                                 self._on_inspection_pose, 10)
        self.create_subscription(PoseStamped, '/hazard/retreat_pose',
                                 self._on_retreat_pose, 10)

        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        self.active_pub = self.create_publisher(Bool, '/stay_alert/active', 10)
        self.mode_pub = self.create_publisher(String, '/stay_alert/mode', 10)
        self.event_pub = self.create_publisher(String, '/stay_alert/event', 10)

        self.create_timer(0.2, self._update)
        self._publish_mode()
        self.get_logger().info(
            f'stay_alert_node iniciado | enter={self.enter_threshold} '
            f'exit={self.exit_threshold} max_invest={self.max_investigation_s}s')

    # ------------------------------------------------------------------ #
    def _on_phi(self, msg: Float64):
        self.phi = msg.data

    def _on_inspection_pose(self, msg: PoseStamped):
        self.target_pose = msg

    def _on_retreat_pose(self, msg: PoseStamped):
        self.retreat_pose = msg

    def _update(self):
        now = self.now_s()

        if self.mode == self.PATROL:
            # repulsão tem prioridade (segurança antes de inspeção), exceto
            # durante o refratário pós-recuo (deixa o keepout/Nav2 contornar)
            if (self.phi <= -self.enter_threshold and self.retreat_pose is not None
                    and now >= self._avoid_until):
                self._enter(self.AVOID, self.retreat_pose, now)
            elif self.phi >= self.enter_threshold and self.target_pose is not None:
                self._enter(self.INVESTIGATE, self.target_pose, now)
            return

        elapsed = now - self._investigate_start
        reached = self._reached_at is not None
        timed_out = elapsed >= self.max_investigation_s

        if self.mode == self.INVESTIGATE:
            # NÃO sair por "cooled" (Φ<exit): a anomalia é marcada visitada no
            # início da investigação, então Φ cai logo após o commit. Concluímos
            # a aproximação (chegou + dwell) ou desistimos por tempo. Isso elimina
            # a oscilação PATROL<->INVESTIGATE no vale de Φ entre anomalias e
            # quando o waypoint fica colado na anomalia.
            if reached and now - self._reached_at >= self.dwell_s:
                self._exit('inspected', elapsed)
            elif timed_out:
                self._exit('timeout', elapsed)

        elif self.mode == self.AVOID:
            if self.phi > -self.exit_threshold:      # repulsão cessou
                self._exit('safe', elapsed)
            elif reached:                            # chegou ao ponto seguro
                self._exit('retreated', elapsed)
            elif timed_out:
                self._exit('timeout', elapsed)

    # ------------------------------------------------------------------ #
    def _enter(self, mode, pose, now):
        self.mode = mode
        self._investigate_start = now
        self._reached_at = None
        self.active_pub.publish(Bool(data=True))     # mission pausa a ronda
        self._publish_mode()
        tag = 'investigate_start' if mode == self.INVESTIGATE else 'avoid_start'
        self.event_pub.publish(String(data=f'{tag} phi={self.phi:.3f}'))
        self._send_goal(pose)
        p = pose.pose.position
        arrow = '>>' if mode == self.INVESTIGATE else '!!'
        self.get_logger().info(
            f'{arrow} {mode} (Phi={self.phi:+.3f}) -> ({p.x:.1f},{p.y:.1f})')

    def _exit(self, reason, elapsed):
        ending = self.mode
        if ending == self.AVOID:   # arma o refratário pós-recuo (C7)
            self._avoid_until = self.now_s() + self.avoid_refractory_s
        self.mode = self.PATROL
        self._cancel_goal()
        self.active_pub.publish(Bool(data=False))    # mission retoma a ronda
        self._publish_mode()
        tag = 'investigate_end' if ending == self.INVESTIGATE else 'avoid_end'
        self.event_pub.publish(
            String(data=f'{tag} reason={reason} dur={elapsed:.1f}'))
        self.get_logger().info(f'<< PATROL (motivo={reason}, {elapsed:.1f}s)')

    # --------------------------- Nav2 goal ----------------------------- #
    def _send_goal(self, pose):
        if not self.nav_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().warn('Nav2 indisponível; ação reativa sem deslocamento')
            return
        goal = NavigateToPose.Goal()
        goal.pose = pose
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        self.nav_client.send_goal_async(goal).add_done_callback(self._on_goal_resp)

    def _on_goal_resp(self, future):
        handle = future.result()
        if not handle.accepted:
            return
        self._goal_handle = handle
        handle.get_result_async().add_done_callback(self._on_goal_done)

    def _on_goal_done(self, _future):
        # chegou ao destino reativo -> marca o instante (dwell/retreated)
        if self.mode in (self.INVESTIGATE, self.AVOID) and self._reached_at is None:
            self._reached_at = self.now_s()

    def _cancel_goal(self):
        if self._goal_handle is not None:
            self._goal_handle.cancel_goal_async()
            self._goal_handle = None

    def _publish_mode(self):
        self.mode_pub.publish(String(data=self.mode))

    def now_s(self) -> float:
        return self.get_clock().now().nanoseconds / 1e9


def main(args=None):
    rclpy.init(args=args)
    node = StayAlertNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
