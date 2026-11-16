#!/usr/bin/env python3
"""Giam toc do tien (linear.x) khi dang re, giup quet map muot va chinh xac hon."""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped


class CmdVelSlowdown(Node):
    def __init__(self):
        super().__init__('cmd_vel_slowdown')
        self.declare_parameter('angular_threshold', 0.2)  # rad/s - vuot nguong nay la coi nhu dang re
        self.declare_parameter('slow_scale', 0.4)          # con lai bao nhieu % toc do tien khi re

        self.angular_threshold = self.get_parameter('angular_threshold').value
        self.slow_scale = self.get_parameter('slow_scale').value

        self.pub = self.create_publisher(TwistStamped, 'cmd_vel', 10)
        self.sub = self.create_subscription(
            TwistStamped, 'cmd_vel_raw', self.cb, 10)

        self.get_logger().info(
            f'cmd_vel_slowdown: threshold={self.angular_threshold} rad/s, '
            f'scale={self.slow_scale}')

    def cb(self, msg: TwistStamped):
        if abs(msg.twist.angular.z) > self.angular_threshold:
            msg.twist.linear.x *= self.slow_scale
            msg.twist.linear.y *= self.slow_scale
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = CmdVelSlowdown()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
