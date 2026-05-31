"""
Nav2 com mapa estático + AMCL (S4 — versão reproduzível p/ experimentos).
========================================================================

Localização por AMCL sobre o mapa estático da subestação (gerado de
gerar_mapa.py, frame `map` alinhado ao mundo). Usa o bringup_launch.py do
nav2 com slam:=False, que sobe map_server + amcl + a pilha de navegação
(controlador MPPI). Pressupõe robot_sim.launch.py já no ar (/scan, /odom, TF).

Uso:
    ros2 launch tese_nav nav2_amcl.launch.py
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = get_package_share_directory('tese_nav')
    nav2_params = os.path.join(pkg, 'config', 'nav2_params_sim.yaml')
    default_map = os.path.join(pkg, 'config', 'maps', 'subestacao.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time')
    map_yaml = LaunchConfiguration('map')

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([
            FindPackageShare('nav2_bringup'), 'launch', 'bringup_launch.py'])),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'slam': 'False',
            'map': map_yaml,
            'params_file': nav2_params,
            'autostart': 'true',
        }.items())

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('map', default_value=default_map),
        nav2,
    ])
