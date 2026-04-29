from pathlib import Path
import yaml

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    rate    = LaunchConfiguration("rate")
    prefix  = LaunchConfiguration("prefix")
    gui     = LaunchConfiguration("gui")
    xbot    = LaunchConfiguration("xbot")

    centauro_urdf_share   = get_package_share_directory("centauro_urdf")
    centauro_srdf_share   = get_package_share_directory("centauro_srdf")
    centauro_ci_share     = get_package_share_directory("centauro_cartesio_config")

    robot_description = Path(centauro_urdf_share, "urdf", "centauro.urdf").read_text()
    robot_description_semantic = Path(centauro_srdf_share, "srdf", "centauro.srdf").read_text()
    problem_description = Path(centauro_ci_share, "centauro_manipulation_stack.yaml").read_text()

    ros_server_remaps_xbot = [
        ("robot_description",          "/xbotcore/robot_description"),
        ("robot_description_semantic", "/xbotcore/robot_description_semantic"),
    ]

    common_ros_server_params = {
        "solver": "OpenSot",
        "rate":   rate,
        "problem_description": problem_description,
        "joint_ctrl_mode": yaml.dump({
            'j_wheel_1': 0,
            'j_wheel_2': 0,
            'j_wheel_3': 0,
            'j_wheel_4': 0,
            'ankle_yaw_1': 0,
            'ankle_yaw_2': 0,
            'ankle_yaw_3': 0,
            'ankle_yaw_4': 0,
            'dagana_1_claw_joint': 0,
            'dagana_2_claw_joint': 0,
            'd435_head_joint': 0,
            'velodyne_joint': 0,
        })
    }

    return LaunchDescription([
        DeclareLaunchArgument("rate",   default_value="100.0"),
        DeclareLaunchArgument("prefix", default_value=""),
        DeclareLaunchArgument("gui",    default_value="false"),
        DeclareLaunchArgument("xbot",   default_value="false"),

        # Robot description publisher (only without xbot)
        Node(
            condition=UnlessCondition(xbot),
            package="cartesian_interface_ros",
            executable="robot_description_publisher",
            name="robot_description_publisher",
            parameters=[{
                "robot_description":          robot_description,
                "robot_description_semantic": robot_description_semantic,
            }],
        ),

        # CartesI/O server — no xbot
        Node(
            condition=UnlessCondition(xbot),
            package="cartesian_interface_ros",
            executable="ros_server_node",
            name="ros_server_node",
            output="screen",
            prefix=prefix,
            parameters=[common_ros_server_params],
        ),

        # CartesI/O server — with xbot (remaps robot_description topics)
        Node(
            condition=IfCondition(xbot),
            package="cartesian_interface_ros",
            executable="ros_server_node",
            name="ros_server_node",
            output="screen",
            prefix=prefix,
            remappings=ros_server_remaps_xbot,
            parameters=[common_ros_server_params],
        ),

        # RViz (optional)
        Node(
            condition=IfCondition(gui),
            package="rviz2",
            executable="rviz2",
            name="rviz",
            arguments=["-d", str(Path(centauro_ci_share, "rviz_cartesio.rviz"))],
        ),

        # Interactive markers
        Node(
            package="cartesian_interface_ros",
            executable="marker_spawner",
            name="interactive_markers",
            output="screen",
        ),
    ])
