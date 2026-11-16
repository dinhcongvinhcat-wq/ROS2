import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_table_bot_description = get_package_share_directory('table_bot_description')

    xacro_file = os.path.join(
        pkg_table_bot_description, 'urdf', 'table_bot.urdf.xacro')

    lidar_serial_port = LaunchConfiguration('lidar_serial_port')
    esp32_serial_port = LaunchConfiguration('esp32_serial_port')

    declare_lidar_port = DeclareLaunchArgument(
        'lidar_serial_port', default_value='/dev/rplidar',
        description='Cong serial cua RPLidar')
    declare_esp32_port = DeclareLaunchArgument(
        'esp32_serial_port', default_value='/dev/esp32',
        description='Cong serial cua ESP32 (gui cmd_vel xuong dong co)')

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
            'serial_port': lidar_serial_port,
            'serial_baudrate': 115200,
            'frame_id': 'lidar_link',
            'inverted': False,
            'angle_compensate': True,
        }],
    )

    rf2o_node = Node(
        package='rf2o_laser_odometry',
        executable='rf2o_laser_odometry_node',
        name='rf2o_laser_odometry',
        output='screen',
        parameters=[{
            'laser_scan_topic': '/scan',
            'odom_topic': '/odom',
            'publish_tf': True,
            'base_frame_id': 'base_link',
            'odom_frame_id': 'odom',
            'init_pose_from_topic': '',
            'freq': 10.0,
            'verbose': False,
        }],
    )

    esp32_bridge_node = Node(
        package='table_bot_base',
        executable='esp32_serial_bridge',
        name='esp32_serial_bridge',
        output='screen',
        parameters=[{
            'serial_port': esp32_serial_port,
            'baudrate': 115200,
        }],
        # rf2o da lo /odom + tf odom->base_link roi, doi topic odom cua
        # esp32_bridge sang ten khac de tranh dam nhau (du hien tai chua
        # co encoder nen se khong publish gi, nhung remap cho an toan).
        remappings=[('odom', 'odom_encoder_unused')],
    )

    return LaunchDescription([
        declare_lidar_port,
        declare_esp32_port,
        robot_state_publisher,
        rplidar_node,
        rf2o_node,
        esp32_bridge_node,
    ])
