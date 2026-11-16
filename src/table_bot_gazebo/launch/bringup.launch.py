import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_table_bot_gazebo = get_package_share_directory('table_bot_gazebo')
    pkg_table_bot_description = get_package_share_directory('table_bot_description')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='-2.0')
    y_pose = LaunchConfiguration('y_pose', default='0.5')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true',
        description='Use simulation (Gazebo) clock if true')
    declare_x = DeclareLaunchArgument('x_pose', default_value='-2.0')
    declare_y = DeclareLaunchArgument('y_pose', default_value='0.5')

    gazebo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_table_bot_gazebo, 'launch', 'gazebo.launch.py')
        )
    )

    rsp_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_table_bot_description, 'launch', 'description.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    spawn_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_table_bot_gazebo, 'launch', 'spawn_robot.launch.py')
        ),
        launch_arguments={'x_pose': x_pose, 'y_pose': y_pose}.items()
    )

    bridge_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_table_bot_gazebo, 'launch', 'bridge.launch.py')
        )
    )

    # Fix mismatch frame_id: gz-sim gop link "lidar_link" (fixed joint) vao
    # "base_link" khi chuyen URDF->SDF, nen /scan bi ghi frame_id la
    # "table_bot/base_link/lidar_sensor" thay vi "lidar_link" nhu TF thuc te.
    # Them 1 transform tinh (0 0 0) noi 2 ten nay lai de Cartographer tra duoc.
    static_tf_lidar_fix = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_lidar_frame_fix',
        arguments=[
            '--x', '0', '--y', '0', '--z', '0',
            '--qx', '0', '--qy', '0', '--qz', '0', '--qw', '1',
            '--frame-id', 'lidar_link',
            '--child-frame-id', 'table_bot/base_link/lidar_sensor',
        ],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    # Cung mot van de nhu lidar o tren: gz-sim gop link "imu_link" (fixed
    # joint) vao "base_link" khi chuyen URDF->SDF, nen /imu bi ghi frame_id
    # la "table_bot/base_link/imu_sensor" thay vi "imu_link" nhu TF thuc te.
    static_tf_imu_fix = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_imu_frame_fix',
        arguments=[
            '--x', '0', '--y', '0', '--z', '0',
            '--qx', '0', '--qy', '0', '--qz', '0', '--qw', '1',
            '--frame-id', 'imu_link',
            '--child-frame-id', 'table_bot/base_link/imu_sensor',
        ],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_x,
        declare_y,
        gazebo_cmd,
        rsp_cmd,
        spawn_cmd,
        bridge_cmd,
        static_tf_lidar_fix,
        static_tf_imu_fix,
    ])
