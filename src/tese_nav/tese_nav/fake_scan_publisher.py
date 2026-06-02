"""
Publica LaserScan sintético (ranges = max_range) para destravar o AMCL e o
Nav2 no WSL, onde o lidar do Gazebo não inicializa por limitação do OGRE no
driver Mesa virtual (GL3PlusTextureGpu::copyTo não implementado no ogre2).

Para os experimentos, o AMCL usa a pose inicial conhecida + este scan "vazio"
(sem obstáculos), enquanto o global_costmap usa o mapa estático. A contribuição
do artigo (Bellman atratora / Stay Alert) não depende de scan real.
"""
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class FakeScanPublisher(Node):
    def __init__(self):
        super().__init__('fake_scan_publisher')
        self.pub = self.create_publisher(LaserScan, '/scan', 10)
        self.create_timer(0.1, self._publish)  # 10 Hz

    def _publish(self):
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_scan'
        msg.angle_min = -math.pi
        msg.angle_max = math.pi
        msg.angle_increment = 2 * math.pi / 360
        msg.time_increment = 0.0
        msg.scan_time = 0.1
        msg.range_min = 0.12
        msg.range_max = 12.0
        msg.ranges = [12.0] * 360  # sem obstáculos detectados
        msg.intensities = []
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = FakeScanPublisher()
    rclpy.spin(node)
    rclpy.shutdown()
