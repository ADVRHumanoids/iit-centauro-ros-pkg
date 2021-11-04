cmake_minimum_required(VERSION 3.0)

set(ROBOT_NAME centauro)
project(iit-${ROBOT_NAME}-ros-pkg VERSION 1.0.0)


## add sub-packages
add_subdirectory(centauro_urdf)

add_subdirectory(centauro_srdf)

include(GenerateDeb.cmake)