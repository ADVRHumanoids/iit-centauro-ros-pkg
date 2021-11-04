cmake_minimum_required(VERSION 3.0)

set(ROBOT_NAME centauro)
project(iit-${ROBOT_NAME}-ros-pkg)


## add sub-packages
add_subdirectory(centauro_urdf)

add_subdirectory(centauro_srdf)

