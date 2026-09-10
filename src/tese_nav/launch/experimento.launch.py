"""
Experimento completo (S5/S6): simulação (robô + Gazebo + Nav2/AMCL/MPPI) +
pilha Stay Alert (Bellman, missão de waypoints, anomalias, métricas).

A pilha Stay Alert sobe com atraso (`sa_delay`) para o Nav2 já estar ativo
quando o mission_node começar a enviar os waypoints.

Uso:
    # E3 (proposto, eta=0.5) headless, com RViz:
    ros2 launch tese_nav experimento.launch.py run_label:=E3 eta:=0.5 rviz:=true
    # E1 baseline (ronda simples, sem desvio):
    ros2 launch tese_nav experimento.launch.py run_label:=E1 enable_stay_alert:=false
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, IncludeLaunchDescription,
                            TimerAction)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg = get_package_share_directory('tese_nav')

    run_label = LaunchConfiguration('run_label')
    eta = LaunchConfiguration('eta')
    enable_stay_alert = LaunchConfiguration('enable_stay_alert')
    headless = LaunchConfiguration('headless')
    rviz = LaunchConfiguration('rviz')
    sa_delay = LaunchConfiguration('sa_delay')
    scenario = LaunchConfiguration('scenario')

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg, 'launch', 'simulation.launch.py')),
        launch_arguments={'headless': headless, 'rviz': rviz}.items())

    stay_alert = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg, 'launch', 'stay_alert.launch.py')),
        launch_arguments={
            'run_label': run_label,
            'eta': eta,
            'enable_stay_alert': enable_stay_alert,
            'enable_anomaly': 'true',
            'use_sim_time': 'true',
            'scenario': scenario,
            'reactive': LaunchConfiguration('reactive'),
            'noise_pos': LaunchConfiguration('noise_pos'),
            'noise_int': LaunchConfiguration('noise_int'),
            'publish_keepout': LaunchConfiguration('publish_keepout'),
            'enable_reactive_avoid': LaunchConfiguration('enable_reactive_avoid'),
            'run_seed': LaunchConfiguration('run_seed'),
        }.items())

    return LaunchDescription([
        DeclareLaunchArgument('run_label', default_value='E3'),
        DeclareLaunchArgument('eta', default_value='0.5'),
        DeclareLaunchArgument('enable_stay_alert', default_value='true'),
        DeclareLaunchArgument('headless', default_value='true'),
        DeclareLaunchArgument('rviz', default_value='false'),
        DeclareLaunchArgument('sa_delay', default_value='45.0',
                              description='Atraso (s) p/ subir o Stay Alert '
                                          'após o Nav2'),
        DeclareLaunchArgument('scenario', default_value='default',
                              description="'default' | 'adverse' | 'route_hazard'"),
        DeclareLaunchArgument('reactive', default_value='stay_alert',
                              description="camada reativa: 'stay_alert'|'apf'|'qdriven'"),
        DeclareLaunchArgument('noise_pos', default_value='0.0',
                              description='σ (m) de ruído na posição do evento (R1#3)'),
        DeclareLaunchArgument('noise_int', default_value='0.0',
                              description='σ de ruído na intensidade do evento (R1#3)'),
        DeclareLaunchArgument('publish_keepout', default_value='false',
                              description='§8: keepout deliberativo (RHM/ablação a,c)'),
        DeclareLaunchArgument('enable_reactive_avoid', default_value='true',
                              description='§8: recuo reativo (false = ablação keepout-só)'),
        DeclareLaunchArgument('run_seed', default_value='0',
                              description='§13: semente por run (ruído independente + registro)'),
        simulation,
        TimerAction(period=sa_delay, actions=[stay_alert]),
    ])
