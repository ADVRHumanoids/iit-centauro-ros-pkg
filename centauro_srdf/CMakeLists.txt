project(${ROBOT_NAME}_srdf)

find_package(catkin REQUIRED)

catkin_package()

## for each config xacro file, generate srdf and mark it for installation

include(../GenerateXrdf.cmake)

generate_srdf(
  XACRO ${ROBOT_NAME}.srdf.xacro 
  CONFIG config/${ROBOT_NAME}.urdf.xacro 
  ADD_TO_ALL TRUE
  GEN_ACM TRUE
)

generate_capsule_srdf_acm(
  CONFIG_NAME ${ROBOT_NAME}
  ADD_TO_ALL TRUE
)

generate_srdf(
  XACRO ${ROBOT_NAME}.srdf.xacro 
  CONFIG config/${ROBOT_NAME}_virtual_frame.urdf.xacro 
  ADD_TO_ALL TRUE
)

## Mark srdf for installation

install(DIRECTORY srdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)