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


## Mark meshes and launch files for installation
install(DIRECTORY meshes
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)


## for each config xacro file, generate urdf and mark it for installation

# this target groups all configs
add_custom_target(${ROBOT_NAME}_urdf_all ALL)

# some shorthands
set(URDF_DIR ${CMAKE_SOURCE_DIR}/${ROBOT_NAME}_urdf/urdf)
set(CONFIG_DIR ${URDF_DIR}/config)

# glob all config xacros
file(GLOB CONFIG_FILE_LIST ${CONFIG_DIR}/*.urdf.xacro)

# generate and install urdf
foreach(CONFIG_FILE ${CONFIG_FILE_LIST})
  
  # config name from file path
  get_filename_component(CONFIG_NAME ${CONFIG_FILE} NAME_WE)
  message(STATUS "[urdf] adding ${CONFIG_NAME} to generation")

  # urdf
  set(URDF_OUTPUT_FILE ${URDF_DIR}/${CONFIG_NAME}.urdf)

  add_custom_target(${CONFIG_NAME}_urdf
    COMMENT "Generating ${URDF_OUTPUT_FILE} .."
    COMMAND rosrun xacro xacro ${URDF_DIR}/${ROBOT_NAME}.urdf.xacro config:=${CONFIG_DIR}/${CONFIG_NAME}.urdf.xacro -o ${URDF_OUTPUT_FILE}
  )

  add_dependencies(${ROBOT_NAME}_urdf_all ${CONFIG_NAME}_urdf)

  install(FILES ${URDF_OUTPUT_FILE}
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  )
endforeach()

