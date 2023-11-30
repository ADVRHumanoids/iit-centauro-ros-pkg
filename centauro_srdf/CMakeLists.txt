cmake_minimum_required(VERSION 3.20)
project(centauro_srdf)

find_package(ament_cmake REQUIRED)

# # main srdf, with acm
# generate_srdf(
#   XACRO ${ROBOT_NAME}.srdf.xacro 
#   CONFIG config/${ROBOT_NAME}.urdf.xacro 
#   ADD_TO_ALL TRUE
#   GEN_ACM TRUE
# )

# # updated acm for capsule model
# generate_capsule_srdf_acm(
#   CONFIG_NAME ${ROBOT_NAME}
#   ADD_TO_ALL TRUE
# )

# # plain srdf for virtual frame model
# generate_srdf(
#   XACRO ${ROBOT_NAME}.srdf.xacro 
#   CONFIG config/${ROBOT_NAME}_virtual_frame.urdf.xacro 
#   ADD_TO_ALL TRUE
# )

# mark srdf for installation
install(DIRECTORY srdf
  DESTINATION share/${PROJECT_NAME}
)

ament_package()