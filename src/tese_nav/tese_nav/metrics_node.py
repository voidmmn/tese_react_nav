"""
Metrics Node — coleta de dados para o artigo IEEE Access.
=========================================================

Centraliza as métricas definidas em S6.1 e grava um CSV com uma linha por
amostra (formato longo: timestamp, metric, value), conveniente para o
pandas/seaborn na análise estatística (S6.4).

Métricas:
  anomalies_detected   - eventos investigate_start únicos por anomalia
  mission_duration_s   - tempo desde o 1º waypoint até COMPLETE
  distance_traveled_m  - integral da odometria
  route_deviations     - de /bellman/route_deviations
  investigation_time_s - tempo acumulado em modo INVESTIGATE
  q_convergence        - TD-error médio (de /bellman/td_error)
"""
import csv
import math
import os
from datetime import datetime

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, Int32, String
from nav_msgs.msg import Odometry

from tese_nav.anomaly_simulator import DEFAULT_HAZARDS


class MetricsNode(Node):

    def __init__(self):
        super().__init__('metrics_node')

        self.declare_parameter('output_dir', os.path.expanduser('~/tese_ws/results'))
        self.declare_parameter('run_label', 'run')
        out_dir = os.path.expanduser(self.get_parameter('output_dir').value)
        label = self.get_parameter('run_label').value
        os.makedirs(out_dir, exist_ok=True)

        stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.path = os.path.join(out_dir, f'metrics_{label}_{stamp}.csv')
        self._fh = open(self.path, 'w', newline='')
        self._csv = csv.writer(self._fh)
        self._csv.writerow(['timestamp', 'metric', 'value'])

        # estado acumulado
        self.distance = 0.0
        self.route_deviations = 0
        self.investigation_time = 0.0
        self.anomalies_detected = 0      # nº de investigate_start (eventos)
        self.anomalies_unique = 0        # nº de anomalias únicas inspecionadas
        self.hazard_avoidances = 0       # nº de eventos de recuo (avoid_start)
        self.min_hazard_dist = float('inf')   # menor distância a um perigo (m)
        self.td_error = 0.0
        self.mission_start = None
        self.mission_end = None
        self._last_xy = None
        self._mode = 'PATROL'
        self._invest_since = None

        self.create_subscription(Odometry, '/odom', self._on_odom, 10)
        self.create_subscription(Int32, '/bellman/route_deviations',
                                 self._on_dev, 10)
        self.create_subscription(Float64, '/bellman/td_error', self._on_td, 10)
        self.create_subscription(String, '/stay_alert/event', self._on_event, 10)
        self.create_subscription(String, '/stay_alert/mode', self._on_mode, 10)
        self.create_subscription(String, '/mission/state', self._on_mission, 10)
        self.create_subscription(Int32, '/anomaly/unique_detected',
                                 self._on_unique, 10)

        self.create_timer(1.0, self._flush_sample)
        self.get_logger().info(f'metrics_node gravando em {self.path}')

    # ------------------------------------------------------------------ #
    def _on_odom(self, msg: Odometry):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        if self._last_xy is not None:
            dx = x - self._last_xy[0]
            dy = y - self._last_xy[1]
            self.distance += (dx * dx + dy * dy) ** 0.5
        self._last_xy = (x, y)
        # menor distância a qualquer perigo ao longo da missão (métrica de segurança)
        for h in DEFAULT_HAZARDS:
            d = math.hypot(x - h['x'], y - h['y'])
            if d < self.min_hazard_dist:
                self.min_hazard_dist = d

    def _on_unique(self, msg: Int32):
        self.anomalies_unique = msg.data

    def _on_dev(self, msg: Int32):
        self.route_deviations = msg.data

    def _on_td(self, msg: Float64):
        self.td_error = msg.data

    def _on_event(self, msg: String):
        if msg.data.startswith('investigate_start'):
            self.anomalies_detected += 1
        elif msg.data.startswith('avoid_start'):
            self.hazard_avoidances += 1

    def _on_mode(self, msg: String):
        now = self.now_s()
        if msg.data == 'INVESTIGATE' and self._mode != 'INVESTIGATE':
            self._invest_since = now
        elif msg.data != 'INVESTIGATE' and self._mode == 'INVESTIGATE':
            if self._invest_since is not None:
                self.investigation_time += now - self._invest_since
                self._invest_since = None
        self._mode = msg.data

    def _on_mission(self, msg: String):
        now = self.now_s()
        if msg.data in ('NAVIGATING', 'PAUSED') and self.mission_start is None:
            self.mission_start = now
        if msg.data == 'COMPLETE' and self.mission_end is None:
            self.mission_end = now
            self.get_logger().info('Missão COMPLETA — métricas finais gravadas.')
            self._flush_sample()

    # ------------------------------------------------------------------ #
    def _flush_sample(self):
        t = self.now_s()
        duration = 0.0
        if self.mission_start is not None:
            end = self.mission_end if self.mission_end else t
            duration = end - self.mission_start

        live_invest = self.investigation_time
        if self._mode == 'INVESTIGATE' and self._invest_since is not None:
            live_invest += t - self._invest_since

        min_haz = (self.min_hazard_dist if self.min_hazard_dist != float('inf')
                   else -1.0)
        rows = {
            'anomalies_detected': self.anomalies_detected,   # eventos de investida
            'anomalies_unique': self.anomalies_unique,       # anomalias únicas
            'mission_duration_s': duration,
            'distance_traveled_m': self.distance,
            'route_deviations': self.route_deviations,
            'investigation_time_s': live_invest,
            'hazard_avoidances': self.hazard_avoidances,     # nº de recuos
            'min_hazard_distance_m': min_haz,                # segurança (maior=melhor)
            'q_convergence': self.td_error,
        }
        for k, v in rows.items():
            self._csv.writerow([f'{t:.3f}', k, v])
        self._fh.flush()

    def now_s(self) -> float:
        return self.get_clock().now().nanoseconds / 1e9

    def destroy_node(self):
        try:
            self._fh.close()
        finally:
            super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = MetricsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
