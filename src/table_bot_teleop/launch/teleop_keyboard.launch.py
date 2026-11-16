"""
Chay teleop ban phim de dieu khien table_bot (dung khi quet map bang Cartographer).

Luu y: cmd_vel cua table_bot dung kieu geometry_msgs/msg/TwistStamped (xem
table_bot_gazebo/params/table_bot_bridge.yaml), nen node teleop_twist_keyboard
phai duoc bat tham so stamped:=true de xuat dung kieu du lieu.

Chay lenh nay trong MOT CUA SO TERMINAL RIENG (can ban phim tuong tac):
    ros2 launch table_bot_teleop teleop_keyboard.launch.py
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    teleop_node = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop_twist_keyboard',
        output='screen',
        prefix='xterm -e',
        parameters=[{'stamped': True, 'frame_id': 'base_link'}],
        remappings=[('cmd_vel', 'cmd_vel_raw')],   # doi ra topic trung gian
    )

    slowdown_node = Node(
        package='table_bot_teleop',
        executable='cmd_vel_slowdown.py',
        name='cmd_vel_slowdown',
        output='screen',
        parameters=[{'angular_threshold': 0.2, 'slow_scale': 0.4}],
    )

    return LaunchDescription([
        teleop_node,
        slowdown_node,
    ])
