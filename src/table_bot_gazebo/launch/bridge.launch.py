import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    bridge_params = os.path.join(
        get_package_share_directory('table_bot_gazebo'),
        'params',
        'table_bot_bridge.yaml'
    )

    bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['--ros-args', '-p', f'config_file:={bridge_params}'],
        output='screen',
    )

    return LaunchDescription([
        bridge_cmd,
    ])
