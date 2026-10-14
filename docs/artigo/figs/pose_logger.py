#!/usr/bin/env python3
"""Loga a pose do robô no frame map (TF map->base_footprint) a 10 Hz num CSV
(t,x,y). Uso: python3 pose_logger.py saida.csv  (após sourcing do ROS)."""
import csv
import sys
import time

import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener, TransformException


class PoseLogger(Node):
    def __init__(self, path):
        super().__init__('pose_logger')
        self.buf = Buffer()
        self.listener = TransformListener(self.buf, self)
        self.f = open(path, 'w', newline='')
        self.w = csv.writer(self.f)
        self.w.writerow(['t', 'x', 'y'])
        self.t0 = time.time()
        self.create_timer(0.1, self.tick)

    def tick(self):
        try:
            tr = self.buf.lookup_transform('map', 'base_footprint',
                                           rclpy.time.Time())
        except TransformException:
            return
        self.w.writerow([f'{time.time()-self.t0:.2f}',
                         f'{tr.transform.translation.x:.3f}',
                         f'{tr.transform.translation.y:.3f}'])
        self.f.flush()


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'traj.csv'
    rclpy.init()
    node = PoseLogger(path)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
