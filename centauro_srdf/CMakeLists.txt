project(${ROBOT_NAME}_srdf)

find_package(catkin REQUIRED)

catkin_package()

## for each config xacro file, generate srdf and mark it for installation

# this target groups all configs
add_custom_target(${ROBOT_NAME}_srdf_all ALL)

# some shorthands
set(URDF_DIR ${CMAKE_SOURCE_DIR}/${ROBOT_NAME}_urdf/urdf)
set(SRDF_DIR ${CMAKE_SOURCE_DIR}/${ROBOT_NAME}_srdf/srdf)
set(CONFIG_DIR ${URDF_DIR}/config)

# glob all config xacros
file(GLOB CONFIG_FILE_LIST ${CONFIG_DIR}/*.urdf.xacro)

# generate and install srdf
foreach(CONFIG_FILE ${CONFIG_FILE_LIST})
  
  # config name from file path
  get_filename_component(CONFIG_NAME ${CONFIG_FILE} NAME_WE)
  message(STATUS "[srdf] adding ${CONFIG_NAME} to generation")

  # srdf
  set(SRDF_OUTPUT_FILE ${SRDF_DIR}/${CONFIG_NAME}.srdf)

  add_custom_target(${CONFIG_NAME}_srdf
    COMMENT "Generating ${SRDF_OUTPUT_FILE} .."
    COMMAND rosrun xacro xacro ${SRDF_DIR}/${ROBOT_NAME}.srdf.xacro config:=${CONFIG_DIR}/${CONFIG_NAME}.urdf.xacro -o ${SRDF_OUTPUT_FILE}
  )

  install(FILES ${SRDF_OUTPUT_FILE}
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  )

  add_dependencies(${ROBOT_NAME}_srdf_all ${CONFIG_NAME}_srdf)

endforeach()
