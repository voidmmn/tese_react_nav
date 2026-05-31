"""
Nav2 + SLAM online (S4).
========================

Sobe o slam_toolbox (online async, gera map->odom) e o bringup de navegação
do Nav2 com os parâmetros da tese (controlador MPPI). Pressupõe que a
simulação do robô (robot_sim.launch.py) já está no ar, fornecendo /scan,
/odom e a TF odom->base_footprint->base_link.

Uso:
    ros2 launch tese_nav nav2.launch.py
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
    slam_params = os.path.join(pkg, 'config', 'slam_toolbox.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time')

    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([
            FindPackageShare('slam_toolbox'), 'launch',
            'online_async_launch.py'])),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'slam_params_file': slam_params,
        }.items())

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([
            FindPackageShare('nav2_bringup'), 'launch',
            'navigation_launch.py'])),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': nav2_params,
        }.items())

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        slam,
        nav2,
    ])
