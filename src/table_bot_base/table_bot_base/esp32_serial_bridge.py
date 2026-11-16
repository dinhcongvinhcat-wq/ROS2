#!/usr/bin/env python3
import math
import time
import threading

import serial
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped


class Esp32SerialBridge(Node):
    def __init__(self):
        super().__init__('esp32_serial_bridge')

        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('wheel_radius', 0.05)
        self.declare_parameter('wheel_separation', 0.36)
        self.declare_parameter('ticks_per_rev', 1320)

        port = self.get_parameter('serial_port').value
        baud = self.get_parameter('baudrate').value
        self.wheel_radius = self.get_parameter('wheel_radius').value
        self.wheel_sep = self.get_parameter('wheel_separation').value
        self.ticks_per_rev = self.get_parameter('ticks_per_rev').value

        self.get_logger().info(f'Dang mo cong serial {port} @ {baud}...')
        self.ser = serial.Serial(port, baud, timeout=0.1)

        self.x = 0.0
        self.y = 0.0
        self.th = 0.0

        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.tf_bcaster = TransformBroadcaster(self)

        self.cmd_sub = self.create_subscription(
            TwistStamped, 'cmd_vel', self.on_cmd_vel, 10)

        self.read_thread = threading.Thread(target=self.read_loop, daemon=True)
        self.read_thread.start()

        self.get_logger().info('esp32_serial_bridge da san sang.')

    def on_cmd_vel(self, msg: TwistStamped):
        v = -msg.twist.linear.x
        w = msg.twist.angular.z
        self.get_logger().info(f'Nhan cmd_vel: v={v:.3f} w={w:.3f}')
        line = f"V {v:.3f} {w:.3f}\n"
        try:
            self.ser.write(line.encode('ascii'))
        except serial.SerialException as e:
            self.get_logger().error(f'Loi ghi serial: {e}')

    def read_loop(self):
        buf = b''
        while rclpy.ok():
            try:
                if self.ser.in_waiting > 0:
                    data = self.ser.read(self.ser.in_waiting)
                else:
                    data = b''
                    time.sleep(0.01)
            except (serial.SerialException, OSError):
                time.sleep(0.1)
                continue
            if not data:
                continue
            buf += data
            while b'\n' in buf:
                line, buf = buf.split(b'\n', 1)
                self.handle_line(line.decode('ascii', errors='ignore').strip())

    def handle_line(self, line: str):
        if not line.startswith('O '):
            return
        parts = line.split()
        if len(parts) != 4:
            return
        try:
            ticks_l = int(parts[1])
            ticks_r = int(parts[2])
            dt_ms = int(parts[3])
        except ValueError:
            return
        if dt_ms <= 0:
            return

        dt = dt_ms / 1000.0
        dist_per_tick = (2.0 * math.pi * self.wheel_radius) / self.ticks_per_rev
        d_left = ticks_l * dist_per_tick
        d_right = ticks_r * dist_per_tick

        d_center = (d_left + d_right) / 2.0
        d_th = (d_right - d_left) / self.wheel_sep

        self.x += d_center * math.cos(self.th + d_th / 2.0)
        self.y += d_center * math.sin(self.th + d_th / 2.0)
        self.th += d_th

        v = d_center / dt
        w = d_th / dt

        now = self.get_clock().now().to_msg()

        odom = Odometry()
        odom.header.stamp = now
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.z = math.sin(self.th / 2.0)
        odom.pose.pose.orientation.w = math.cos(self.th / 2.0)
        odom.twist.twist.linear.x = v
        odom.twist.twist.angular.z = w
        self.odom_pub.publish(odom)

        tf = TransformStamped()
        tf.header.stamp = now
        tf.header.frame_id = 'odom'
        tf.child_frame_id = 'base_link'
        tf.transform.translation.x = self.x
        tf.transform.translation.y = self.y
        tf.transform.rotation.z = math.sin(self.th / 2.0)
        tf.transform.rotation.w = math.cos(self.th / 2.0)
        self.tf_bcaster.sendTransform(tf)


def main(args=None):
    rclpy.init(args=args)
    node = Esp32SerialBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
