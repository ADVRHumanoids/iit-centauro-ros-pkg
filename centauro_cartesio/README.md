# Cartesian control examples with *CartesI/O*
*CartesI/O* is a software architecture for online (and *real-time*) Cartesian control, which allows the user to configure a Cartesian controller from a configuration file in the popular YAML format.
Based on this description, it auto-generates many ROS interfaces that are used to interact with the controller. Both python and C++ client libraries are available. The following examples use the python client library in order to perform some example manipulation and wheeled locomotion tasks with the Pholus robot.

**Wiki** https://github.com/ADVRHumanoids/XBotControl/wiki/CartesIO

**Cite our work!** https://ieeexplore.ieee.org/document/8794464

## Manipulation example
How to run:
- `roslaunch pholus_cartesio pholus_manipulation.launch` (requires having this package inside `ROS_PACKAGE_PATH` environment variable)
- to visualize the solver state in RViz: `roslaunch pholus_cartesio pholus_manipulation.launch gui:=true`
- to move the left end effector with a marker, right click on it -> select `continuous control` -> move it around
- run the demo by invoking the python script `manipulation_example.py`

## Wheeled motion example
Dependency: `libcentauro_cartesio_addon.so` must be found inside env `LD_LIBRARY_PATH`

How to run:
- `roslaunch pholus_cartesio pholus_wheeled_motion.launch` (requires having this package inside `ROS_PACKAGE_PATH` environment variable)
- to visualize the solver state in RViz: `roslaunch pholus_cartesio pholus_wheeled_motion.launch gui:=true`
- to move the robot with wheels with a marker, change the marker topic to the `pelvis` marker, right click on it -> select `continuous control` -> move it around
- run the demo by invoking the python script `wheeled_motion_example.py`
