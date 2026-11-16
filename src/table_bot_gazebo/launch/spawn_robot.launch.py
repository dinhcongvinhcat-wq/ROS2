from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    x_pose = LaunchConfiguration('x_pose', default='-2.0')
    y_pose = LaunchConfiguration('y_pose', default='0.5')
    z_pose = LaunchConfiguration('z_pose', default='0.05')

    declare_x = DeclareLaunchArgument('x_pose', default_value='-2.0')
    declare_y = DeclareLaunchArgument('y_pose', default_value='0.5')
    declare_z = DeclareLaunchArgument('z_pose', default_value='0.05')

    spawn_cmd = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'table_bot',
            '-topic', 'robot_description',
            '-x', x_pose,
            '-y', y_pose,
            '-z', z_pose,
        ],
        output='screen',
    )

    return LaunchDescription([
        declare_x,
        declare_y,
        declare_z,
        spawn_cmd,
    ])
