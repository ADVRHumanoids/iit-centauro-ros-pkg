function(generate_xrdf type)

    cmake_parse_arguments(GEN_XRDF "ADD_TO_ALL" "XACRO;CONFIG" "" ${ARGN})
    
    # config name from file path
    get_filename_component(CONFIG_NAME ${GEN_XRDF_CONFIG} NAME_WE)
    message(STATUS "[${type}] adding ${GEN_XRDF_CONFIG} to generation ")

    set(URDF_DIR ${CMAKE_SOURCE_DIR}/${ROBOT_NAME}_urdf/urdf)
    set(SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/${type})
    set(CONFIG_ABSPATH ${URDF_DIR}/${GEN_XRDF_CONFIG})
    set(XACRO_ABSPATH ${SRC_DIR}/${GEN_XRDF_XACRO})

    # ${type}
    set(OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/${CONFIG_NAME}.${type})

    add_custom_target(generate_${type}_${CONFIG_NAME}
        COMMENT "Generating ${OUTPUT_FILE} .."
        COMMAND rosrun xacro xacro ${XACRO_ABSPATH} config:=${CONFIG_ABSPATH} -o ${OUTPUT_FILE}
    )

    # install rule
    install(FILES ${OUTPUT_FILE}
        DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
    )

    # publish to source folder
    add_custom_target(publish_${type}_${CONFIG_NAME}
        COMMENT "Publishing ${OUTPUT_FILE} to ${SRC_DIR}"
        COMMAND cp ${OUTPUT_FILE} ${SRC_DIR}
    )

    add_dependencies(publish_${type}_${CONFIG_NAME} generate_${type}_${CONFIG_NAME})

    if(${GEN_XRDF_ADD_TO_ALL})
        if(NOT TARGET generate_${type}_all)
            add_custom_target(generate_${type}_all ALL)
        endif()
        if(NOT TARGET publish_${type}_all)
            add_custom_target(publish_${type}_all)
        endif()
        add_dependencies(publish_${type}_all publish_${type}_${CONFIG_NAME})
        add_dependencies(generate_${type}_all generate_${type}_${CONFIG_NAME})
    endif()

endfunction()

function(generate_urdf)
    generate_xrdf(urdf ${ARGV})
endfunction()

function(generate_srdf)
    generate_xrdf(srdf ${ARGV})
endfunction()