import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_table_bot_navigation = get_package_share_directory('table_bot_navigation')

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    map_dir = LaunchConfiguration(
        'map',
        default=os.path.expanduser('~/ros2/maps/my_map.yaml'))

    param_dir = LaunchConfiguration(
        'params_file',
        default=os.path.join(pkg_table_bot_navigation, 'param', 'table_bot.yaml'))

    nav2_launch_file_dir = os.path.join(
        get_package_share_directory('nav2_bringup'), 'launch')

    rviz_config_dir = os.path.join(
        pkg_table_bot_navigation, 'rviz', 'table_bot_navigation2.rviz')

    return LaunchDescription([
        DeclareLaunchArgument(
            'map', default_value=map_dir,
            description='Full path to map yaml file to load'),
        DeclareLaunchArgument(
            'params_file', default_value=param_dir,
            description='Full path to nav2 param file to load'),
        DeclareLaunchArgument(
            'use_sim_time', default_value='false',
            description='Use simulation clock (false for real robot)'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_launch_file_dir, '/bringup_launch.py']),
            launch_arguments={
                'map': map_dir,
                'use_sim_time': use_sim_time,
                'params_file': param_dir,
                'slam': 'False',
                'autostart': 'True'}.items(),
        ),

     
    ])
