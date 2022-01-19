project(${ROBOT_NAME}_urdf)

find_package(catkin REQUIRED COMPONENTS)

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if your package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES pholus_urdf
#  CATKIN_DEPENDS joint_state_publisher robot_state_publisher rospy
#  DEPENDS system_lib
)


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


## for each config xacro file, generate urdf and mark it for installation
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
)