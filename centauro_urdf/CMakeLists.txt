project(${ROBOT_NAME}_urdf)

find_package(catkin REQUIRED COMPONENTS)

catkin_package()


## Mark urdf, meshes and launch files for installation
install(DIRECTORY meshes
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY urdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)


## for each config xacro file, generate urdf
include(../GenerateXrdf.cmake)

generate_urdf(
  XACRO ${ROBOT_NAME}.urdf.xacro 
  CONFIG config/${ROBOT_NAME}.urdf.xacro 
  ADD_TO_ALL TRUE
)

generate_urdf(
  XACRO ${ROBOT_NAME}.urdf.xacro 
  CONFIG config/${ROBOT_NAME}_virtual_frame.urdf.xacro 
  ADD_TO_ALL TRUE
)

generate_capsule_urdf(
  CONFIG_NAME ${ROBOT_NAME}
  ADD_TO_ALL TRUE
)