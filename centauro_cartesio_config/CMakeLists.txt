cmake_minimum_required(VERSION 3.8)
project(centauro_cartesio_config)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)

install(
  FILES 
  centauro_manipulation_stack.yaml
  centauro_manipulation.launch 
  DESTINATION share/${PROJECT_NAME}/
)

# Testing
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
endif()

# Export dependencies
ament_export_dependencies()

ament_package()
