"""
Robô + Gazebo Harmonic + ponte ros_gz (S2).
===========================================

Sobe o mundo da subestação no gz-sim, spawna o inspector_bot a partir do
/robot_description (publicado pelo robot_state_publisher) e abre a ponte de
tópicos ROS2 <-> gz. Base para o S4 (Nav2).

Uso:
    ros2 launch tese_nav robot_sim.launch.py            # headless (sem GUI)
    ros2 launch tese_nav robot_sim.launch.py headless:=false   # com GUI
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, ExecuteProcess,
                            SetEnvironmentVariable)
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('tese_nav')
    world = os.path.join(pkg, 'worlds', 'subestacao.sdf')
    urdf = os.path.join(pkg, 'urdf', 'inspector_bot.urdf')
    bridge_cfg = os.path.join(pkg, 'config', 'bridge.yaml')

    with open(urdf) as f:
        robot_desc = f.read()

    headless = LaunchConfiguration('headless')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')

    # ign-gazebo (Fortress) server-only (headless) ou completo (com GUI)
    gz_headless = ExecuteProcess(
        cmd=['ign', 'gazebo', '-s', '-r', '-v', '2', world],
        output='screen', condition=IfCondition(headless))
    gz_gui = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', '-v', '2', world],
        output='screen', condition=UnlessCondition(headless))

    robot_state_publisher = Node(
        package='robot_state_publisher', executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}])

    spawn = Node(
        package='ros_gz_sim', executable='create', output='screen',
        arguments=['-topic', 'robot_description', '-name', 'inspector_bot',
                   '-x', x, '-y', y, '-z', '0.10'])

    bridge = Node(
        package='ros_gz_bridge', executable='parameter_bridge', output='screen',
        parameters=[{'config_file': bridge_cfg, 'use_sim_time': True}])

    # O /scan vem do gz com frame_id escopado (inspector_bot/base_footprint/
    # lidar); o Fortress não tem <gz_frame_id>. Ligamos esse frame ao base_scan
    # do robot_state_publisher com uma TF estática identidade, para o Nav2
    # encontrar o frame do laser na árvore TF.
    scan_tf = Node(
        package='tf2_ros', executable='static_transform_publisher', output='screen',
        arguments=['--frame-id', 'base_scan',
                   '--child-frame-id', 'inspector_bot/base_footprint/lidar'])

    return LaunchDescription([
        # Isola gz (ign-transport) E ROS (DDS) na loopback: evita o discovery
        # confuso por múltiplas interfaces (ex.: docker0 em 172.17.0.1).
        SetEnvironmentVariable('IGN_IP', '127.0.0.1'),
        SetEnvironmentVariable('IGN_PARTITION', 'tese_sim'),
        SetEnvironmentVariable('ROS_LOCALHOST_ONLY', '1'),

        DeclareLaunchArgument('headless', default_value='true',
                              description='true = gz sim -s (sem GUI)'),
        DeclareLaunchArgument('x', default_value='-10.0',
                              description='Posição inicial X do robô'),
        DeclareLaunchArgument('y', default_value='-10.0',
                              description='Posição inicial Y do robô'),
        gz_headless,
        gz_gui,
        robot_state_publisher,
        spawn,
        bridge,
        scan_tf,
    ])
