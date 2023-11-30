cmake_minimum_required(VERSION 3.20)
project(centauro_gazebo)

find_package(ament_cmake REQUIRED)

ament_package()

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY worlds
  DESTINATION share/${PROJECT_NAME}
)
