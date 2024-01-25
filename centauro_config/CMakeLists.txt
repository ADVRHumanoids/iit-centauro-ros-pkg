cmake_minimum_required(VERSION 3.20)
project(centauro_config)

find_package(ament_cmake REQUIRED)

install(DIRECTORY hal
  DESTINATION share/${PROJECT_NAME}
)

install(FILES centauro_basic.yaml 
  DESTINATION share/${PROJECT_NAME}
)

ament_package()