"""
Pilha Stay Alert (sem Gazebo/Nav2): bellman, stay_alert, anomaly simulator,
mission e metrics. Inclua sobre o stack de navegação (ver experimento.launch.py)
ou rode isolada para testar a lógica com /odom de um bag.

Args:
    run_label         rótulo do experimento gravado no CSV (E1..E5)
    eta               peso do campo atrator (sobrescreve bellman_params.yaml)
    enable_stay_alert true = Bellman+StayAlert ativos; false = baseline (só
                      ronda Nav2 + métricas + anomalias, sem desvio) — E1
    enable_anomaly    liga o simulador de anomalias
    use_sim_time      true em simulação (relógio do Gazebo)

Uso:
    ros2 launch tese_nav stay_alert.launch.py run_label:=E3 eta:=0.5
    ros2 launch tese_nav stay_alert.launch.py run_label:=E1 enable_stay_alert:=false
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg = get_package_share_directory('tese_nav')
    params = os.path.join(pkg, 'config', 'bellman_params.yaml')

    run_label = LaunchConfiguration('run_label')
    eta = LaunchConfiguration('eta')
    enable_stay_alert = LaunchConfiguration('enable_stay_alert')
    enable_anomaly = LaunchConfiguration('enable_anomaly')
    use_sim_time = LaunchConfiguration('use_sim_time')
    scenario = LaunchConfiguration('scenario')
    reactive = LaunchConfiguration('reactive')   # 'stay_alert' | 'apf' | 'qdriven'

    # condições combinadas: camada afetiva ligada E qual mecanismo reativo
    def when(mech):
        return IfCondition(PythonExpression(
            ["'", enable_stay_alert, "' == 'true' and '", reactive, "' == '", mech, "'"]))

    sim = {'use_sim_time': ParameterValue(use_sim_time, value_type=bool)}
    eta_p = {'eta': ParameterValue(eta, value_type=float)}
    scen_p = {'scenario': scenario}
    # keepout deliberativo (C7) é a expressão da repulsão afetiva -> só quando a
    # camada afetiva está ligada (baseline E1 não projeta e passa reto no perigo)
    keepout_p = {'publish_keepout': ParameterValue(enable_stay_alert, value_type=bool)}
    # ruído de percepção (R1#3): sweep de robustez; default 0 = percepção ideal
    noise_p = {
        'noise_position_std': ParameterValue(
            LaunchConfiguration('noise_pos'), value_type=float),
        'noise_intensity_std': ParameterValue(
            LaunchConfiguration('noise_int'), value_type=float),
    }

    return LaunchDescription([
        DeclareLaunchArgument('run_label', default_value='E3'),
        DeclareLaunchArgument('eta', default_value='0.5'),
        DeclareLaunchArgument('enable_stay_alert', default_value='true'),
        DeclareLaunchArgument('enable_anomaly', default_value='true'),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('scenario', default_value='default'),
        DeclareLaunchArgument('reactive', default_value='stay_alert',
                              description="camada reativa: 'stay_alert'|'apf'|'qdriven'"),
        DeclareLaunchArgument('noise_pos', default_value='0.0'),
        DeclareLaunchArgument('noise_int', default_value='0.0'),

        # Método proposto (Stay Alert): bellman + FSM afetivo
        Node(package='tese_nav', executable='bellman_node',
             name='bellman_node', output='screen',
             parameters=[params, eta_p, sim],
             condition=when('stay_alert')),
        Node(package='tese_nav', executable='stay_alert_node',
             name='stay_alert_node', output='screen',
             parameters=[params, sim],
             condition=when('stay_alert')),

        # Baseline APF (campo potencial) — mesma patrulha Nav2, camada reativa
        Node(package='tese_nav', executable='apf_node',
             name='apf_node', output='screen',
             parameters=[params, sim, scen_p],
             condition=when('apf')),

        # Baseline Q-driven (RL comportamental, Q pré-treinada greedy)
        Node(package='tese_nav', executable='qdriven_node',
             name='qdriven_node', output='screen',
             parameters=[params, sim, scen_p],
             condition=when('qdriven')),

        # Sempre presentes: ronda, métricas, anomalias
        Node(package='tese_nav', executable='mission_node',
             name='mission_node', output='screen',
             parameters=[params, sim]),
        Node(package='tese_nav', executable='metrics_node',
             name='metrics_node', output='screen',
             parameters=[params, sim, scen_p, {'run_label': run_label}]),
        Node(package='tese_nav', executable='anomaly_simulator',
             name='anomaly_simulator', output='screen',
             parameters=[params, sim, scen_p, keepout_p, noise_p],
             condition=IfCondition(enable_anomaly)),
    ])
