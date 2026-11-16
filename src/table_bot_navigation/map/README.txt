Thu muc nay chua ban do (map.yaml + map.pgm) dung cho Nav2.

=== QUY TRINH QUET MAP VA CHAY NAV2 (trong ros2_ws) ===

1) Build workspace (lan dau, hoac sau khi doi package):
   cd ~/ros2_ws
   colcon build --symlink-install
   source install/setup.bash

2) Bat mo phong + Cartographer SLAM:
   ros2 launch table_bot_cartographer start_mapping.launch.py

3) Mo THEM MOT TERMINAL khac (nho source install/setup.bash), dieu khien xe
   chay khap khu vuc de quet het ban do:
   ros2 launch table_bot_teleop teleop_keyboard.launch.py
   (hoac: ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true)

4) Khi ban do da quet du, luu lai bang lenh (o mot terminal khac):
   ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/table_bot_navigation/map/map --ros-args -p save_map_timeout:=10.0

   Lenh nay tao ra 2 file: map.yaml va map.pgm trong thu muc nay.

5) Dong Cartographer/Gazebo, build lai package de file map duoc cai vao share/:
   cd ~/ros2_ws
   colcon build --packages-select table_bot_navigation --symlink-install
   source install/setup.bash

6) Chay Nav2 voi ban do vua luu:
   ros2 launch table_bot_navigation navigation2.launch.py
