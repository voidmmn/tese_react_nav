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
from std_msgs.msg import Float64, Bool, String, Int32
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus


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
        # §8 ablação: desliga o RECUO reativo (mantém investigação). Permite o
        # experimento (a) keepout-só vs (b) recuo-só vs (c) ambos.
        self.declare_parameter('enable_reactive_avoid', True)

        self.enter_threshold = self.get_parameter('enter_threshold').value
        self.exit_threshold = self.get_parameter('exit_threshold').value
        self.max_investigation_s = self.get_parameter('max_investigation_s').value
        self.dwell_s = self.get_parameter('dwell_s').value
        self.avoid_refractory_s = self.get_parameter('avoid_refractory_s').value
        self.enable_reactive_avoid = self.get_parameter('enable_reactive_avoid').value
        self._avoid_until = 0.0   # instante até o qual AVOID fica bloqueado

        self.mode = self.PATROL
        self.phi = 0.0
        self._investigate_start = None
        self.target_pose = None       # pose de inspeção (atração)
        self.retreat_pose = None      # pose de recuo (repulsão)
        self._goal_handle = None       # goal Nav2 corrente (investigação/recuo)
        self._reached_at = None        # quando chegou ao destino (SÓ em SUCCEEDED)
        self._goal_epoch = 0           # id do episódio reativo corrente
        self._nav_outcome = None       # último desfecho Nav2 (diag/métricas)
        self._target_id = -1           # §10: id do evento-alvo (ecoado do simulador)

        self.create_subscription(Float64, '/stay_alert/attraction', self._on_phi, 10)
        self.create_subscription(PoseStamped, '/anomaly/inspection_pose',
                                 self._on_inspection_pose, 10)
        self.create_subscription(PoseStamped, '/hazard/retreat_pose',
                                 self._on_retreat_pose, 10)
        self.create_subscription(Int32, '/anomaly/target_id',
                                 self._on_target_id, 10)

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

    def _on_target_id(self, msg: Int32):
        self._target_id = msg.data   # §10: id do evento-alvo mais saliente

    def _on_retreat_pose(self, msg: PoseStamped):
        self.retreat_pose = msg

    def _update(self):
        now = self.now_s()

        # §7.1 PREEMPÇÃO DE SEGURANÇA: um perigo acima do limiar interrompe
        # QUALQUER estado (Patrol OU Investigate) e força AVOID — a precedência
        # categórica de Phi (Eq. 4) vale mesmo durante uma aproximação já em
        # curso, não só na patrulha. O guard do refratário pós-recuo preserva o
        # hand-off reflexo->keepout deliberativo (documentado no Algoritmo 1).
        if (self.enable_reactive_avoid
                and self.mode != self.AVOID
                and self.phi <= -self.enter_threshold
                and self.retreat_pose is not None
                and now >= self._avoid_until):
            if self.mode == self.INVESTIGATE:   # §10: investigação preemptada por perigo
                self._exit('deferred_hazard', now - self._investigate_start)
            self._enter(self.AVOID, self.retreat_pose, now)
            return

        if self.mode == self.PATROL:
            # sem perigo preemptivo: só a atração pode tirar da patrulha
            if self.phi >= self.enter_threshold and self.target_pose is not None:
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
            elif self._nav_outcome in ('aborted', 'canceled', 'rejected'):
                self._exit('failed', elapsed)   # não espera o timeout após falha
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
        # §5.2 (3ª rodada): zera o desfecho de navegação AO INICIAR o episódio.
        # Sem isso, um 'aborted' do episódio ANTERIOR persistia e o _update
        # encerrava a investigação NOVA como 'failed' já no 1º tick (antes de a
        # nova meta ser aceita). O desfecho passa a valer só para este episódio.
        self._nav_outcome = None
        self._goal_epoch += 1                        # novo episódio reativo
        self.active_pub.publish(Bool(data=True))     # mission pausa a ronda
        self._publish_mode()
        tag = 'investigate_start' if mode == self.INVESTIGATE else 'avoid_start'
        # §10: ecoa o id do evento-alvo p/ o simulador creditar por identidade
        eid = self._target_id if mode == self.INVESTIGATE else -1
        self.event_pub.publish(String(data=f'{tag} id={eid} phi={self.phi:.3f}'))
        self._send_goal(pose, self._goal_epoch)
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
        self._goal_epoch += 1                        # encerra o episódio: callbacks tardios viram stale
        self.active_pub.publish(Bool(data=False))    # mission retoma a ronda
        self._publish_mode()
        tag = 'investigate_end' if ending == self.INVESTIGATE else 'avoid_end'
        self.event_pub.publish(
            String(data=f'{tag} reason={reason} dur={elapsed:.1f}'))
        self.get_logger().info(f'<< PATROL (motivo={reason}, {elapsed:.1f}s)')

    # --------------------------- Nav2 goal ----------------------------- #
    def _send_goal(self, pose, epoch):
        if not self.nav_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().warn('Nav2 indisponível; ação reativa sem deslocamento')
            self._nav_outcome = 'unavailable'
            return
        goal = NavigateToPose.Goal()
        goal.pose = pose
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        self.nav_client.send_goal_async(goal).add_done_callback(
            lambda f: self._on_goal_resp(f, epoch))

    def _on_goal_resp(self, future, epoch):
        handle = future.result()
        if epoch != self._goal_epoch:
            # §5.3: resposta TARDIA de um episódio já encerrado -> cancela a meta
            # se foi aceita, para o robô não perseguir um objetivo obsoleto
            if handle is not None and handle.accepted:
                handle.cancel_goal_async()
            return
        if not handle.accepted:                      # REJEITADO é desfecho próprio
            self._nav_outcome = 'rejected'
            self.event_pub.publish(String(data='nav_result outcome=rejected'))
            self.get_logger().warn('Nav2 REJEITOU a meta reativa')
            return
        self._goal_handle = handle
        handle.get_result_async().add_done_callback(
            lambda f: self._on_goal_done(f, epoch))

    def _on_goal_done(self, future, epoch):
        # callback de episódio anterior (meta cancelada) NÃO conclui o atual
        if epoch != self._goal_epoch:
            return
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self._nav_outcome = 'succeeded'
            # chegou de fato ao destino reativo -> marca o instante (dwell/retreated)
            if self.mode in (self.INVESTIGATE, self.AVOID) and self._reached_at is None:
                self._reached_at = self.now_s()
        else:                                        # ABORTED/CANCELED/outro: NÃO é chegada
            name = {GoalStatus.STATUS_ABORTED: 'aborted',
                    GoalStatus.STATUS_CANCELED: 'canceled'}.get(status, f'status{status}')
            self._nav_outcome = name
            self.event_pub.publish(String(data=f'nav_result outcome={name}'))
            self.get_logger().warn(f'navegação reativa não concluída: {name}')

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
