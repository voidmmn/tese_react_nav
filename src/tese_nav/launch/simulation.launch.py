"""
Simulação completa do S4: robô no Gazebo Fortress + ponte ros_gz + Nav2 com
mapa estático e AMCL (controlador MPPI). Ponto de entrada único.

Sobe robot_sim primeiro e, após um atraso (para o robô spawnar e a TF
odom->base_footprint->base_link começar a fluir ANTES do Nav2 subir — evita
a corrida de TF no boot dos costmaps), inclui o nav2_amcl. Opcionalmente abre
o RViz para inspeção visual (recomendado durante o ajuste fino da navegação).

Uso:
    ros2 launch tese_nav simulation.launch.py                # headless + sem rviz
    ros2 launch tese_nav simulation.launch.py rviz:=true     # com RViz (precisa de tela)
    ros2 launch tese_nav simulation.launch.py headless:=false rviz:=true
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, IncludeLaunchDescription,
                            SetEnvironmentVariable, TimerAction)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('tese_nav')

    headless = LaunchConfiguration('headless')
    rviz = LaunchConfiguration('rviz')
    nav_delay = LaunchConfiguration('nav_delay')

    robot_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg, 'launch', 'robot_sim.launch.py')),
        launch_arguments={'headless': headless}.items())

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg, 'launch', 'nav2_amcl.launch.py')),
        launch_arguments={'use_sim_time': 'true'}.items())

    # Nav2 só depois que o robô spawnou e a TF está fluindo.
    nav2_delayed = TimerAction(period=nav_delay, actions=[nav2])

    # Config pronta do Nav2 (RobotModel, TF, Map, costmaps, Path, e a
    # ferramenta "Nav2 Goal"); Fixed Frame = map.
    rviz_cfg = os.path.join(
        get_package_share_directory('nav2_bringup'), 'rviz',
        'nav2_default_view.rviz')
    rviz_node = Node(
        package='rviz2', executable='rviz2', name='rviz2', output='screen',
        condition=IfCondition(rviz),
        arguments=['-d', rviz_cfg],
        parameters=[{'use_sim_time': True}])

    return LaunchDescription([
        # ROS na loopback (evita discovery DDS confuso por múltiplas
        # interfaces, ex.: docker0) — espelha o IGN_IP do gz.
        SetEnvironmentVariable('ROS_LOCALHOST_ONLY', '1'),

        DeclareLaunchArgument('headless', default_value='true'),
        DeclareLaunchArgument('rviz', default_value='false'),
        DeclareLaunchArgument('nav_delay', default_value='12.0',
                              description='Segundos antes de subir o Nav2'),

        robot_sim,
        nav2_delayed,
        rviz_node,
    ])
