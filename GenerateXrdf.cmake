function(generate_xrdf type)

    cmake_parse_arguments(GEN_XRDF "ADD_TO_ALL;GEN_ACM" "XACRO;CONFIG" "" ${ARGN})
    
    # config name from file path
    get_filename_component(CONFIG_NAME ${GEN_XRDF_CONFIG} NAME_WE)
    message(STATUS "[${type}] adding ${GEN_XRDF_CONFIG} to generation ")

    set(URDF_DIR ${CMAKE_SOURCE_DIR}/${ROBOT_NAME}_urdf/urdf)
    set(SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/${type})
    set(CONFIG_ABSPATH ${URDF_DIR}/${GEN_XRDF_CONFIG})
    set(XACRO_ABSPATH ${SRC_DIR}/${GEN_XRDF_XACRO})
    set(URDF_FILE ${CMAKE_BINARY_DIR}/${ROBOT_NAME}_urdf/${CONFIG_NAME}.urdf)

    file(GLOB_RECURSE XACRO_FILES ${SRC_DIR}/*.${type}.xacro)
    file(GLOB_RECURSE CONFIG_FILES ${URDF_DIR}/config/*.urdf.xacro)
    
    # generate target and corresponding command
    set(OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/${CONFIG_NAME}.${type})

    # conditional generation of acm
    if(${GEN_XRDF_GEN_ACM})
        set(GEN_ACM_DEPENDS "${URDF_FILE}")
        set(GEN_ACM_CMD moveit_compute_default_collisions --urdf_path ${URDF_FILE} --srdf_path ${OUTPUT_FILE})
    endif()

    add_custom_target(generate_${type}_${CONFIG_NAME}
        DEPENDS ${OUTPUT_FILE})

    add_custom_command(
        OUTPUT ${OUTPUT_FILE}
        COMMENT "Generating ${OUTPUT_FILE} .."
        COMMAND rosrun xacro xacro ${XACRO_ABSPATH} config:=${CONFIG_ABSPATH} -o ${OUTPUT_FILE}
        COMMAND ${GEN_ACM_CMD}
        DEPENDS ${XACRO_FILES} ${CONFIG_FILES} ${GEN_ACM_DEPENDS}
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

function(generate_capsule_urdf)
    
    cmake_parse_arguments(GEN_CAPSULE "ADD_TO_ALL" "CONFIG_NAME" "" ${ARGN})
    set(CONFIG_NAME ${GEN_CAPSULE_CONFIG_NAME})
    set(OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/${CONFIG_NAME}_capsule.urdf)
    set(SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/urdf)
    set(GEN_CAPSULE_URDF ${CMAKE_CURRENT_BINARY_DIR}/${CONFIG_NAME}.urdf)
    set(CAPSULE_FOLDER ${CMAKE_CURRENT_BINARY_DIR}/capsules)
    if(${GEN_CAPSULE_ADD_TO_ALL})
        set(ALL_OPT ALL)
    endif()

    add_custom_target(generate_urdf_${CONFIG_NAME}_capsule
        ${ALL_OPT}
        DEPENDS ${OUTPUT_FILE}
        DEPENDS generate_urdf_${CONFIG_NAME}
    )

    add_custom_command(
        OUTPUT ${OUTPUT_FILE}
        COMMENT "Generating ${OUTPUT_FILE} .."
        COMMAND mkdir -p ${CAPSULE_FOLDER}
        COMMAND robot_capsule_urdf ${GEN_CAPSULE_URDF} --output ${OUTPUT_FILE} -c ${CAPSULE_FOLDER}
        COMMAND robot_capsule_urdf_to_rviz ${OUTPUT_FILE} --output ${OUTPUT_FILE}
        DEPENDS ${XACRO_FILES} ${GEN_CAPSULE_URDF}
    )

    add_custom_target(publish_urdf_${CONFIG_NAME}_capsule
        DEPENDS ${OUTPUT_FILE}
        COMMENT "Publishing ${OUTPUT_FILE} to ${SRC_DIR}"
        COMMAND cp ${OUTPUT_FILE} ${SRC_DIR}
    )

    if(${GEN_CAPSULE_ADD_TO_ALL})
        add_dependencies(publish_urdf_all publish_urdf_${CONFIG_NAME}_capsule)
    endif()

endfunction()

function(generate_capsule_srdf_acm)
    
    cmake_parse_arguments(GEN_CAPSULE "ADD_TO_ALL" "CONFIG_NAME" "" ${ARGN})
    set(CONFIG_NAME ${GEN_CAPSULE_CONFIG_NAME})

    set(OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/${CONFIG_NAME}_capsule.srdf)
    set(URDF_FILE ${CMAKE_BINARY_DIR}/${ROBOT_NAME}_urdf/${CONFIG_NAME}_capsule.urdf)
    set(SRDF_FILE ${CMAKE_CURRENT_BINARY_DIR}/${CONFIG_NAME}.srdf)
    set(SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/srdf)
    if(${GEN_CAPSULE_ADD_TO_ALL})
        set(ALL_OPTION ALL)
    endif()

    add_custom_target(generate_srdf_${CONFIG_NAME}_capsule
        ${ALL_OPTION}
        DEPENDS ${OUTPUT_FILE}
    )

    add_custom_command(
        OUTPUT ${OUTPUT_FILE}
        DEPENDS ${URDF_FILE} ${SRDF_FILE}
        DEPENDS generate_urdf_${CONFIG_NAME}_capsule generate_srdf_${CONFIG_NAME}
        COMMENT "Generating default collisions for ${URDF_FILE} into ${OUTPUT_FILE}"
        COMMAND cp ${SRDF_FILE} ${OUTPUT_FILE}
        COMMAND moveit_compute_default_collisions --urdf_path ${URDF_FILE} --srdf_path ${OUTPUT_FILE}
    )

    add_custom_target(publish_srdf_${CONFIG_NAME}_capsule
        COMMENT "Publishing ${OUTPUT_FILE} to ${SRC_DIR}"
        COMMAND cp ${OUTPUT_FILE} ${SRC_DIR}
        DEPENDS generate_srdf_${CONFIG_NAME}_capsule
    )

    if(${GEN_CAPSULE_ADD_TO_ALL})
        add_dependencies(publish_srdf_all publish_srdf_${CONFIG_NAME}_capsule)
    endif()

endfunction()