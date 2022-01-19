cmake_minimum_required(VERSION 3.0)
project(centauro_config)

find_package(catkin REQUIRED)

catkin_package()

install(DIRECTORY configs
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY hal
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(FILES centauro_basic.yaml 
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
