cmake_minimum_required(VERSION 3.20)
project(centauro_urdf)

find_package(ament_cmake REQUIRED)

# mark urdf, meshes and launch files for installation
install(DIRECTORY meshes
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}
)

# # main urdf
# generate_urdf(
#   XACRO ${ROBOT_NAME}.urdf.xacro 
#   CONFIG config/${ROBOT_NAME}.urdf.xacro 
#   ADD_TO_ALL TRUE
# )

# # virtual frame urdf
# generate_urdf(
#   XACRO ${ROBOT_NAME}.urdf.xacro 
#   CONFIG config/${ROBOT_NAME}_virtual_frame.urdf.xacro 
#   ADD_TO_ALL TRUE
# )

# # capsule model for main urdf
# generate_capsule_urdf(
#   CONFIG_NAME ${ROBOT_NAME}
#   ADD_TO_ALL TRUE
# )

# ament
ament_package()
