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
from tf2_ros import Buffer, TransformListener, TransformException

from tese_nav.anomaly_simulator import scenario_events


class MetricsNode(Node):

    def __init__(self):
        super().__init__('metrics_node')

        self.declare_parameter('output_dir', os.path.expanduser('~/tese_ws/results'))
        self.declare_parameter('run_label', 'run')
        self.declare_parameter('run_seed', -1)   # §13: semente da run (reprodutib.)
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
        self.anomalies_detected = 0      # nº de investigate_start (commits)
        self.anomalies_unique = 0        # nº de anomalias inspeção CONCLUÍDA
        self.investigation_timeouts = 0  # investigate_end reason=timeout (R2#8)
        self.hazard_avoidances = 0       # nº de eventos de recuo (avoid_start)
        self.investigation_deferred = 0  # §10: investida interrompida por perigo
        self.nav_aborted = 0             # §6/§13: navegações reativas ABORTED
        self.nav_canceled = 0            # §6/§13: CANCELED
        self.nav_rejected = 0            # §6/§13: REJEITADAS pelo Nav2
        self.min_hazard_dist = float('inf')   # menor distância a um perigo (m)
        self.td_error = 0.0
        self.update_residual = 0.0       # |alpha*td + eta*Phi| (resíduo completo)
        # --- segurança (R2#6/R3#2/R4#3): só significativas no cenário
        #     perigo-sobre-a-rota, mas medidas em qualquer cenário ---
        self.collisions = 0              # nº de entradas em raio de colisão
        self._in_collision = False       # borda p/ não recontar o mesmo evento
        self.time_below_clearance = 0.0  # s abaixo da folga de segurança
        self.safety_zone_violations = 0  # nº de entradas na zona de folga
        self._in_clearance = False
        self.min_ttc = float('inf')      # menor tempo-para-colisão (s)
        self.avoid_success = 0           # recuos concluídos (safe/retreated)
        self.avoid_timeout = 0           # recuos abortados por tempo
        self._prev_haz_dist = None
        self._prev_haz_t = None
        self.mission_start = None
        self.mission_end = None
        self._last_xy = None
        self._mode = 'PATROL'
        self._invest_since = None

        # distância ao perigo precisa da pose no frame MAP (igual ao
        # anomaly_simulator): /odom está deslocado do spawn. Integral de
        # distância percorrida pode usar /odom (é relativa).
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('robot_frame', 'base_footprint')
        self.declare_parameter('scenario', 'default')
        self.declare_parameter('collision_radius', 0.5)    # m: contato efetivo
        self.declare_parameter('clearance_threshold', 2.0) # m: zona de folga
        self.map_frame = self.get_parameter('map_frame').value
        self.robot_frame = self.get_parameter('robot_frame').value
        self.collision_radius = self.get_parameter('collision_radius').value
        self.clearance_threshold = self.get_parameter('clearance_threshold').value
        self._hazards = scenario_events(self.get_parameter('scenario').value)[1]
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.create_subscription(Odometry, '/odom', self._on_odom, 10)
        self.create_subscription(Int32, '/bellman/route_deviations',
                                 self._on_dev, 10)
        self.create_subscription(Float64, '/bellman/td_error', self._on_td, 10)
        self.create_subscription(Float64, '/bellman/update_residual',
                                 self._on_residual, 10)
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
        # menor distância a qualquer perigo (segurança) — no frame map via TF
        try:
            t = self.tf_buffer.lookup_transform(
                self.map_frame, self.robot_frame, rclpy.time.Time())
        except TransformException:
            return
        mx, my = t.transform.translation.x, t.transform.translation.y
        if not self._hazards:
            return
        d_now = min(math.hypot(mx - h['x'], my - h['y']) for h in self._hazards)
        if d_now < self.min_hazard_dist:
            self.min_hazard_dist = d_now

        now = self.now_s()
        # colisão (borda de entrada no raio de contato)
        if d_now < self.collision_radius:
            if not self._in_collision:
                self.collisions += 1
                self._in_collision = True
        else:
            self._in_collision = False
        # tempo/violações abaixo da folga de segurança
        if d_now < self.clearance_threshold:
            if not self._in_clearance:
                self.safety_zone_violations += 1
                self._in_clearance = True
            if self._prev_haz_t is not None:
                self.time_below_clearance += now - self._prev_haz_t
        else:
            self._in_clearance = False
        # tempo-para-colisão: dist / velocidade de aproximação ao perigo
        if self._prev_haz_dist is not None and self._prev_haz_t is not None:
            dt = now - self._prev_haz_t
            if dt > 1e-3:
                closing = (self._prev_haz_dist - d_now) / dt   # >0 = aproximando
                if closing > 1e-3:
                    ttc = d_now / closing
                    if ttc < self.min_ttc:
                        self.min_ttc = ttc
        self._prev_haz_dist = d_now
        self._prev_haz_t = now

    def _on_unique(self, msg: Int32):
        self.anomalies_unique = msg.data

    def _on_dev(self, msg: Int32):
        self.route_deviations = msg.data

    def _on_td(self, msg: Float64):
        self.td_error = msg.data

    def _on_residual(self, msg: Float64):
        self.update_residual = msg.data

    def _on_event(self, msg: String):
        d = msg.data
        if d.startswith('investigate_start'):
            self.anomalies_detected += 1
        elif d.startswith('investigate_end'):
            if 'reason=timeout' in d:
                self.investigation_timeouts += 1
            elif 'reason=deferred_hazard' in d:     # §10
                self.investigation_deferred += 1
        elif d.startswith('avoid_start'):
            self.hazard_avoidances += 1
        elif d.startswith('avoid_end'):
            if 'reason=timeout' in d:
                self.avoid_timeout += 1
            else:                                   # safe | retreated
                self.avoid_success += 1
        elif d.startswith('nav_result'):            # §6/§13: desfechos de navegação
            if 'outcome=aborted' in d:
                self.nav_aborted += 1
            elif 'outcome=canceled' in d:
                self.nav_canceled += 1
            elif 'outcome=rejected' in d:
                self.nav_rejected += 1

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
            'anomalies_detected': self.anomalies_detected,   # commits (investida)
            'anomalies_unique': self.anomalies_unique,       # inspeção concluída
            'investigation_timeouts': self.investigation_timeouts,  # abortadas p/ tempo
            'mission_duration_s': duration,
            'distance_traveled_m': self.distance,
            'route_deviations': self.route_deviations,
            'investigation_time_s': live_invest,
            'hazard_avoidances': self.hazard_avoidances,     # nº de recuos
            'min_hazard_distance_m': min_haz,                # segurança (maior=melhor)
            'collisions': self.collisions,
            'time_below_clearance_s': self.time_below_clearance,
            'safety_zone_violations': self.safety_zone_violations,
            'min_ttc_s': (self.min_ttc if self.min_ttc != float('inf') else -1.0),
            'avoid_success': self.avoid_success,
            'avoid_timeout': self.avoid_timeout,
            'q_convergence': self.td_error,           # proxy SEM termo afetivo
            'update_residual': self.update_residual,  # |alpha*td+eta*Phi| completo
            'investigation_deferred': self.investigation_deferred,  # §10
            'nav_aborted': self.nav_aborted,          # §6/§13 desfechos de navegação
            'nav_canceled': self.nav_canceled,
            'nav_rejected': self.nav_rejected,
            'run_seed': self.get_parameter('run_seed').value,  # §13 reprodutibilidade
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
