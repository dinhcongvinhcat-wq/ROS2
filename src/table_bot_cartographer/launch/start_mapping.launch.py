"""
Launch tong hop: bat mo phong Gazebo + spawn table_bot + cau Cartographer SLAM.

Cach dung:
    ros2 launch table_bot_cartographer start_mapping.launch.py

Sau khi RViz hien ban do dang quet, mo mot terminal khac de dieu khien xe:
    ros2 launch table_bot_teleop teleop_keyboard.launch.py

Quet het khu vuc roi luu ban do (xem huong dan trong table_bot_navigation/map/README.txt):
    ros2 run nav2_map_server map_saver_cli -f <duong_dan_ws>/src/table_bot_navigation/map/map --ros-args -p save_map_timeout:=10.0
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_table_bot_gazebo = get_package_share_directory('table_bot_gazebo')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    bringup_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_table_bot_gazebo, 'launch', 'bringup.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )

    cartographer_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('table_bot_cartographer'),
                'launch', 'cartographer.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time', default_value='true',
            description='Use simulation (Gazebo) clock if true'),
        bringup_cmd,
        cartographer_cmd,
    ])
