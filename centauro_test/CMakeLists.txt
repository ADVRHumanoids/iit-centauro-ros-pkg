cmake_minimum_required(VERSION 3.8)
project(centauro_test)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)

add_test(
    NAME gz
    COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/gz_test.py
)

# Testing
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
endif()

# Export dependencies
ament_export_dependencies()

ament_package()