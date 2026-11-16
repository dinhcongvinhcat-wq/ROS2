cmake_minimum_required(VERSION 3.5)
project(table_bot_teleop)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)
install(PROGRAMS
  scripts/cmd_vel_slowdown.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
