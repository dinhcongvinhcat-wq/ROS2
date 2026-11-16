cmake_minimum_required(VERSION 3.5)
project(table_bot_gazebo)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch params
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
