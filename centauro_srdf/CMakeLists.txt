project(${ROBOT_NAME}_srdf)

find_package(catkin REQUIRED)

catkin_package()

## for each config xacro file, generate srdf and mark it for installation

# this target groups all configs
add_custom_target(generate_srdf_all ALL)
add_custom_target(publish_srdf_all)

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
  set(SRDF_OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/${CONFIG_NAME}.srdf)

  add_custom_target(generate_srdf_${CONFIG_NAME}
    COMMENT "Generating ${SRDF_OUTPUT_FILE} .."
    COMMAND rosrun xacro xacro ${SRDF_DIR}/${ROBOT_NAME}.srdf.xacro config:=${CONFIG_DIR}/${CONFIG_NAME}.urdf.xacro -o ${SRDF_OUTPUT_FILE}
  )

  add_dependencies(generate_srdf_all generate_srdf_${CONFIG_NAME})

  # publish to source folder
  add_custom_target(publish_srdf_${CONFIG_NAME}
    COMMENT "Publishing ${SRDF_OUTPUT_FILE} to ${SRDF_DIR}"
    COMMAND cp ${SRDF_OUTPUT_FILE} ${SRDF_DIR}
  )

  add_dependencies(publish_srdf_${CONFIG_NAME} generate_srdf_${CONFIG_NAME})
  add_dependencies(publish_srdf_all publish_srdf_${CONFIG_NAME})

  # install rule
  install(FILES ${SRDF_OUTPUT_FILE}
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  )


endforeach()
