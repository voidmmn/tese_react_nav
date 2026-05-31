"""
Mission Node — gerenciador da ronda de inspeção.
================================================

Carrega os waypoints de inspeção (waypoints.yaml) e os envia ao Nav2 via a
ação NavigateToPose, um a um. Quando o stay_alert_node sinaliza investigação
(/stay_alert/active = True), a missão é pausada; ao retomar, segue para o
próximo waypoint.

Publica /mission/state (String) e /mission/waypoint_index (Int32) para o
metrics_node.
"""
import math
import os

import yaml

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from std_msgs.msg import Bool, String, Int32
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus

from ament_index_python.packages import get_package_share_directory


def yaw_to_quat(yaw: float):
    return (0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0))


class MissionNode(Node):

    def __init__(self):
        super().__init__('mission_node')

        default_wp = os.path.join(
            get_package_share_directory('tese_nav'), 'config', 'waypoints.yaml')
        self.declare_parameter('waypoints_file', default_wp)
        wp_file = self.get_parameter('waypoints_file').value

        self.waypoints = self._load_waypoints(wp_file)
        self.index = 0
        self.paused = False
        self._goal_active = False
        self._goal_handle = None

        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        self.create_subscription(Bool, '/stay_alert/active', self._on_alert, 10)
        self.state_pub = self.create_publisher(String, '/mission/state', 10)
        self.wp_pub = self.create_publisher(Int32, '/mission/waypoint_index', 10)

        self.create_timer(1.0, self._tick)
        self.get_logger().info(
            f'mission_node: {len(self.waypoints)} waypoints carregados de {wp_file}')

    # ------------------------------------------------------------------ #
    def _load_waypoints(self, path):
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            return data.get('waypoints', [])
        except FileNotFoundError:
            self.get_logger().warn(f'waypoints.yaml não encontrado em {path}')
            return []

    def _on_alert(self, msg: Bool):
        was_paused = self.paused
        self.paused = msg.data
        # ao entrar em pausa (Stay Alert assumiu), cancela o waypoint atual
        # para liberar o Nav2 para a investigação; NÃO avança o índice.
        if self.paused and not was_paused and self._goal_handle is not None:
            self.get_logger().info('Stay Alert ativo: cancelando waypoint atual')
            self._goal_handle.cancel_goal_async()
            self._goal_handle = None
            self._goal_active = False

    # ------------------------------------------------------------------ #
    def _tick(self):
        if self.index >= len(self.waypoints):
            self.state_pub.publish(String(data='COMPLETE'))
            return
        if self.paused:
            self.state_pub.publish(String(data='PAUSED'))
            return
        if self._goal_active:
            self.state_pub.publish(String(data='NAVIGATING'))
            return

        self._send_current_waypoint()

    def _send_current_waypoint(self):
        wp = self.waypoints[self.index]
        if not self.nav_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().warn('Nav2 navigate_to_pose indisponível; aguardando…')
            return

        goal = NavigateToPose.Goal()
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = float(wp['x'])
        pose.pose.position.y = float(wp['y'])
        qx, qy, qz, qw = yaw_to_quat(float(wp.get('yaw', 0.0)))
        pose.pose.orientation.z = qz
        pose.pose.orientation.w = qw
        goal.pose = pose

        self._goal_active = True
        self.wp_pub.publish(Int32(data=self.index))
        self.get_logger().info(
            f"-> WP[{self.index}] {wp.get('name', '')} "
            f"({wp['x']:.1f},{wp['y']:.1f})")

        fut = self.nav_client.send_goal_async(goal)
        fut.add_done_callback(self._on_goal_response)

    def _on_goal_response(self, future):
        handle = future.result()
        if not handle.accepted:
            self.get_logger().warn('Goal rejeitado pelo Nav2')
            self._goal_active = False
            return
        self._goal_handle = handle
        handle.get_result_async().add_done_callback(self._on_goal_result)

    def _on_goal_result(self, future):
        status = future.result().status
        self._goal_active = False
        self._goal_handle = None
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.index += 1     # waypoint concluído: avança
        else:
            # cancelado/abortado (ex.: pausa do Stay Alert ou preempção):
            # NÃO avança — o mesmo waypoint é reenviado ao retomar a ronda
            self.get_logger().info(f'WP[{self.index}] não concluído (status {status}); '
                                   'será reenviado')


def main(args=None):
    rclpy.init(args=args)
    node = MissionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
