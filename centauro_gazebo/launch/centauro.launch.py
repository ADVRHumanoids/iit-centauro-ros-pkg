
import os
from subprocess import check_output

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node


def generate_launch_description():
    # Configure ROS nodes for launch

    # Setup project paths
    pkg_centauro_gazebo = get_package_share_directory('centauro_gazebo')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Load the SDF file from "description" package
    xacro_file  =  os.path.join(pkg_centauro_gazebo, 'urdf', 'centauro_gazebo.urdf.xacro')
    robot_desc = check_output(f'xacro {xacro_file}', shell=True).decode()

    # Simulator launch file
    world_file = pkg_centauro_gazebo + '/world/centauro.world'
    include_gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(pkg_ros_gz_sim + '/launch/gz_sim.launch.py'),
        launch_arguments={
            'gz_args': world_file
        }.items()
    )

    # Spawn robot
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        name='urdf_spawner',
        parameters=[{
            'string': robot_desc,
            'z': 1.0,
        }]
    )

    return LaunchDescription([
        include_gz_sim_launch,
        spawn_robot
    ])