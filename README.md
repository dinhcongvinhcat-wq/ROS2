# yahboom_rosmaster #
![OS](https://img.shields.io/ubuntu/v/ubuntu-wallpapers/noble)
![ROS_2](https://img.shields.io/ros/v/jazzy/rclcpp)

Automatic Addison support for the ROSMASTER X3 mecanum wheel robot robot by Yahboom - ROS 2

![ROSMASTER X3 in Gazebo](https://automaticaddison.com/wp-content/uploads/2024/11/gazebo-800-square-mecanum-controller.gif)

![ROSMASTER X3 in RViz](https://automaticaddison.com/wp-content/uploads/2024/11/rviz-800-square-mecanum-controller.gif)



---

## table_bot: dieu khien - quet map (SLAM) - Nav2

Cac package sau duoc gop tu workspace `robot/cartographer_ws/table_bot` vao day de
chay chung trong `ros2_ws`:

| Package | Chuc nang |
|---|---|
| `table_bot_description` | URDF/xacro cua table_bot (co lidar 2D) |
| `table_bot_gazebo` | Bringup mo phong Gazebo (world, spawn, ros_gz_bridge) |
| `table_bot_cartographer` | Cau hinh Cartographer SLAM + launch quet map tong hop |
| `table_bot_navigation` | Cau hinh Nav2 (AMCL, bt_navigator...) + noi luu map.yaml/map.pgm |
| `table_bot_teleop` | Launch dieu khien xe bang ban phim khi quet map |

### Yeu cau truoc khi build

Cac goi sau **khong** duoc chep source vao day (de tranh trung lap build nang
nhu Cartographer/turtlebot3), ban can co san 1 trong 2 cach:

- **Cach A (khuyen nghi neu da co san):** source workspace `cartographer_ws` da
  build truoc do (chua cartographer_ros, turtlebot3_gazebo...) TRUOC KHI source
  `ros2_ws`, vi du trong `~/.bashrc`:
  ```bash
  source ~/robot/cartographer_ws/install/setup.bash
  source ~/ros2_ws/install/setup.bash
  ```
- **Cach B:** cai ban binary neu ROS distro co san:
  ```bash
  sudo apt install ros-jazzy-cartographer ros-jazzy-cartographer-ros \
                    ros-jazzy-turtlebot3-simulations ros-jazzy-nav2-bringup \
                    ros-jazzy-teleop-twist-keyboard
  ```

### Build

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

### Quy trinh quet map va chay Nav2

1. Bat mo phong + Cartographer SLAM:
   ```bash
   ros2 launch table_bot_cartographer start_mapping.launch.py
   ```
2. O mot terminal khac, dieu khien xe quet het khu vuc:
   ```bash
   ros2 launch table_bot_teleop teleop_keyboard.launch.py
   ```
3. Luu ban do (o terminal khac):
   ```bash
   ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/table_bot_navigation/map/map --ros-args -p save_map_timeout:=10.0
   ```
4. Build lai de cai file map, roi chay Nav2:
   ```bash
   colcon build --packages-select table_bot_navigation --symlink-install
   source install/setup.bash
   ros2 launch table_bot_navigation navigation2.launch.py
   ```

Chi tiet them trong `src/table_bot_navigation/map/README.txt`.

**Luu y:** cmd_vel cua table_bot dung kieu `geometry_msgs/msg/TwistStamped`
(xem `table_bot_gazebo/params/table_bot_bridge.yaml`), nen teleop phai bat
tham so `stamped:=true`.
