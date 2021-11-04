cmake_minimum_required(VERSION 3.0)
project(centauro_cartesio_config)

find_package(catkin REQUIRED)

catkin_package()

install(
  FILES 
  centauro_manipulation_stack.yaml
  centauro_manipulation.launch 
  DESTINATION 
  ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
