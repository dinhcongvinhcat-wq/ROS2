import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_table_bot_description = get_package_share_directory('table_bot_description')
    pkg_table_bot_bringup = get_package_share_directory('table_bot_bringup')
    pkg_table_bot_cartographer = get_package_share_directory('table_bot_cartographer')

    xacro_file = os.path.join(
        pkg_table_bot_description, 'urdf', 'table_bot.urdf.xacro')

    rviz_config_dir = os.path.join(
        pkg_table_bot_cartographer, 'rviz', 'table_bot_cartographer.rviz')

    serial_port = LaunchConfiguration('serial_port')

    declare_serial_port = DeclareLaunchArgument(
        'serial_port', default_value='/dev/rplidar',
        description='Cong serial cua RPLidar')

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': ParameterValue(
                Command(['xacro ', xacro_file]), value_type=str),
            'use_sim_time': False,
        }],
    )

    rplidar_node = Node(
        name='rplidar_composition',
        package='rplidar_ros',
        executable='rplidar_composition',
        output='screen',
        parameters=[{
            'serial_port': serial_port,
            'serial_baudrate': 115200,  # RPLidar A1 / A2
            'frame_id': 'lidar_link',   # khop dung ten link trong URDF, khong can static tf fix
            'inverted': False,
            'angle_compensate': True,
        }],
    )

    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        output='screen',
        parameters=[{'use_sim_time': False}],
        arguments=[
            '-configuration_directory', os.path.join(pkg_table_bot_bringup, 'config'),
            '-configuration_basename', 'table_bot_real_2d.lua',
        ],
    )

    occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='cartographer_occupancy_grid_node',
        output='screen',
        parameters=[{'use_sim_time': False}],
        arguments=['-resolution', '0.05', '-publish_period_sec', '1.0'],
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_dir],
        output='screen',
        parameters=[{'use_sim_time': False}],
    )

    return LaunchDescription([
        declare_serial_port,
        robot_state_publisher,
        rplidar_node,
        cartographer_node,
        occupancy_grid_node,
        rviz_node,
    ])
