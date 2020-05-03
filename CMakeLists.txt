cmake_minimum_required(VERSION 2.8)
PROJECT(iit-centauro-ros-pkg)

add_custom_target(  acm
                    COMMAND ${CMAKE_SOURCE_DIR}/centauro_urdf/script/create_acm.sh centauro)

add_custom_target(	remove_old_centauro_urdf_gazebo ALL
    				COMMAND ${CMAKE_COMMAND} -E remove_directory 
        			"~/.gazebo/models/centauro_urdf/")

add_custom_target(  remove_old_centauro_gazebo ALL
                    COMMAND ${CMAKE_COMMAND} -E remove_directory 
                    "~/.gazebo/models/centauro/")

add_custom_target(  compile_urdf_sdf ALL
                    COMMAND ${CMAKE_SOURCE_DIR}/centauro_urdf/script/create_urdf_srdf_sdf.sh centauro)

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    add_custom_target(	copy_centauro_gazebo ALL
        				COMMAND ${CMAKE_COMMAND} -E copy_directory 
            			"${PROJECT_SOURCE_DIR}/centauro_gazebo/sdf/" 
            			"~/.gazebo/models/centauro/"
            			DEPENDS remove_old_centauro_gazebo)
endif()
