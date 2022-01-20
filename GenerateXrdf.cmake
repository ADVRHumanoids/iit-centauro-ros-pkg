# create main targets 
if(NOT TARGET generate)
    add_custom_target(generate)
endif()

if(NOT TARGET publish)
    add_custom_target(publish)
endif()

# generate warning if plain make is invoked
add_custom_target(print_usage
    ALL
    COMMAND echo 'Note \(for developers\): use \"make generate\" to generate urdf and srdf to the build tree, \"make publish\" to copy the results to the source tree'
)

# function to generate urdf and srdf from xacros; this is an internal
# function which is not supposed to be called directly: use generate_urdf, 
# generate_srdf
function(generate_xrdf type)

    cmake_parse_arguments(GEN_XRDF "ADD_TO_ALL;GEN_ACM" "XACRO;CONFIG" "" ${ARGN})
    
    # config name from file path
    get_filename_component(CONFIG_NAME ${GEN_XRDF_CONFIG} NAME_WE)
    message(STATUS "[${type}] adding ${GEN_XRDF_CONFIG} to generation ")

    set(URDF_DIR ${CMAKE_SOURCE_DIR}/${ROBOT_NAME}_urdf/urdf)
    set(SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/${type})

    if(IS_ABSOLUTE ${GEN_XRDF_CONFIG})
        set(CONFIG_ABSPATH ${GEN_XRDF_CONFIG})
    else()
        set(CONFIG_ABSPATH ${URDF_DIR}/${GEN_XRDF_CONFIG})
    endif()

    if(IS_ABSOLUTE ${GEN_XRDF_XACRO})
        set(XACRO_ABSPATH ${GEN_XRDF_CONFIG})
    else()
        set(XACRO_ABSPATH ${SRC_DIR}/${GEN_XRDF_XACRO})
    endif()

    # path to the urdf file (used only if type == srdf to compute acm)
    set(URDF_FILE ${CMAKE_BINARY_DIR}/${ROBOT_NAME}_urdf/${CONFIG_NAME}.urdf)

    # files that the generated xrdf depends upon
    file(GLOB_RECURSE XACRO_FILES ${SRC_DIR}/*.${type}.xacro)
    file(GLOB_RECURSE CONFIG_FILES ${URDF_DIR}/config/*.urdf.xacro)
    
    # generate target and corresponding command
    set(OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/${CONFIG_NAME}.${type})

    # conditional generation of acm
    if(${GEN_XRDF_GEN_ACM})
        set(GEN_ACM_DEPENDS generate_urdf_${CONFIG_NAME})
        set(GEN_ACM_CMD moveit_compute_default_collisions --urdf_path ${URDF_FILE} --srdf_path ${OUTPUT_FILE})
    endif()

    # target and command to perform the actual generation
    add_custom_target(generate_${type}_${CONFIG_NAME}
        DEPENDS ${OUTPUT_FILE} ${GEN_ACM_DEPENDS})

    add_custom_command(
        OUTPUT ${OUTPUT_FILE}
        COMMENT "Generating ${OUTPUT_FILE} .."
        COMMAND rosrun xacro xacro ${XACRO_ABSPATH} config:=${CONFIG_ABSPATH} -o ${OUTPUT_FILE}
        COMMAND ${GEN_ACM_CMD}
        DEPENDS ${XACRO_FILES} ${CONFIG_FILES} 
    )
    message(STATUS "custom cmd with output=${OUTPUT_FILE}, depends=${GEN_ACM_DEPENDS}")

    # publish to source folder
    add_custom_target(publish_${type}_${CONFIG_NAME}
        COMMENT "Publishing ${OUTPUT_FILE} to ${SRC_DIR}"
        COMMAND cp ${OUTPUT_FILE} ${SRC_DIR}
    )

    add_dependencies(publish_${type}_${CONFIG_NAME} generate_${type}_${CONFIG_NAME})

    # add to main targets
    if(${GEN_XRDF_ADD_TO_ALL})
        add_dependencies(publish publish_${type}_${CONFIG_NAME})
        add_dependencies(generate generate_${type}_${CONFIG_NAME})
    endif()

endfunction()


# generate_urdf
# Generate the urdf from a xacro file, with a given configuration file folding
# variables to customize the generation
# 
# Usage:
#   generate_urdf(
#     XACRO <path-to-main-xacro-file>     (if not absolute, base directory is ${ROBOT_NAME}_urdf/urdf)
#     CONFIG <path-to-config-xacro-file>  (if not absolute, base directory is ${ROBOT_NAME}_urdf/urdf)
#     [ADD_TO_ALL TRUE|FALSE]
#   ) 
#
# If ADD_TO_ALL is enabled, this urdf file is generated/published with the default target generate, publish.
# 
function(generate_urdf)
    generate_xrdf(urdf ${ARGV})
endfunction()


# generate_srdf
# Generate the srdf from a xacro file, with a given configuration file folding
# variables to customize the generation. Optionally, this method also generates
# an Allowed Collision Matrix (ACM) in the form of <disable_collision> srdf tags.
# 
# Usage:
#   generate_srdf(
#     XACRO <path-to-main-xacro-file>     (if not absolute, base directory is ${ROBOT_NAME}_srdf/srdf)
#     CONFIG <path-to-config-xacro-file>  (if not absolute, base directory is ${ROBOT_NAME}_urdf/urdf)
#     [ADD_TO_ALL FALSE]
#     [GEN_ACM FALSE]
#   ) 
#
# If ADD_TO_ALL is enabled, this urdf file is generated/published with the default target generate, publish.
# 
function(generate_srdf)
    generate_xrdf(srdf ${ARGV})
endfunction()


# generate_capsule_urdf
# Generate the capsule collisin model from a generated urdf.
# 
# Usage:
#   generate_capsule_urdf(
#     CONFIG_NAME <config-xacro-name> 
#     [ADD_TO_ALL TRUE|FALSE]
#   ) 
#
# Note that CONFIG_NAME is the basename of the xacro config file that was used to generate the urdf,
# for which the capsule model is to be generated.
# If ADD_TO_ALL is enabled, this urdf file is generated/published with the default target generate, publish.
#
function(generate_capsule_urdf)
    
    cmake_parse_arguments(GEN_CAPSULE "ADD_TO_ALL" "CONFIG_NAME" "" ${ARGN})
    set(CONFIG_NAME ${GEN_CAPSULE_CONFIG_NAME})
    set(OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/${CONFIG_NAME}_capsule.urdf)
    set(SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/urdf)
    set(GEN_CAPSULE_URDF ${CMAKE_CURRENT_BINARY_DIR}/${CONFIG_NAME}.urdf)
    set(CAPSULE_FOLDER ${CMAKE_CURRENT_BINARY_DIR}/capsules)

    add_custom_target(generate_urdf_${CONFIG_NAME}_capsule
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
        add_dependencies(generate generate_urdf_${CONFIG_NAME}_capsule)
        add_dependencies(publish publish_urdf_${CONFIG_NAME}_capsule)
    endif()

endfunction()


# generate_capsule_srdf_acm
# Generate the Allowed Collision Matrix (ACM) in the form of <disable_collision> srdf tags,
# corresponding to the capsule urdf based on the provided config file.
# 
# Usage:
#   generate_capsule_srdf_acm(
#     CONFIG_NAME <config-xacro-name> 
#     [ADD_TO_ALL TRUE|FALSE]
#   ) 
#
# If ADD_TO_ALL is enabled, this urdf file is generated/published with the default target generate, publish.
# 
function(generate_capsule_srdf_acm)
    
    cmake_parse_arguments(GEN_CAPSULE "ADD_TO_ALL" "CONFIG_NAME" "" ${ARGN})
    set(CONFIG_NAME ${GEN_CAPSULE_CONFIG_NAME})

    set(OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/${CONFIG_NAME}_capsule.srdf)
    set(URDF_FILE ${CMAKE_BINARY_DIR}/${ROBOT_NAME}_urdf/${CONFIG_NAME}_capsule.urdf)
    set(SRDF_FILE ${CMAKE_CURRENT_BINARY_DIR}/${CONFIG_NAME}.srdf)
    set(SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/srdf)

    add_custom_target(generate_srdf_${CONFIG_NAME}_capsule
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
        add_dependencies(generate generate_srdf_${CONFIG_NAME}_capsule)
        add_dependencies(publish publish_srdf_${CONFIG_NAME}_capsule)
    endif()

endfunction()