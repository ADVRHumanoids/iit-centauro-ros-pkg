# iit-centauro-ros-pkg  [![Build Status](https://app.travis-ci.com/ADVRHumanoids/iit-centauro-ros-pkg.svg?branch=master)](https://app.travis-ci.com/ADVRHumanoids/iit-centauro-ros-pkg)
Repository dedicated to the IIT robot CENTAURO

How to run the simulator
========================
To run the simulator under the [Xbot2](https://advrhumanoids.github.io/xbot2/master/quickstart.html#install-the-xbot2-framework) framework, please follow these steps:
1) install the required dependencies (mainly ROS, Gazebo, and Xbot2 - see the `.travis.yml` file)
2) clone the repository to a sourced environment (e.g., a catkin workspace)
3) set a basic configuration file for Xbot2 with `set_xbot2_config $(rospack find centauro_config)/centauro_basic.yaml`
4) [terminal #1] `mon launch centauro_gazebo centauro_world.launch`  (or `roslaunch` if you don't have `rosmon` installed)
5) [terminal #2] `xbot2-core --simtime`
6) follow instructions and tutorials from [our examples repository](https://github.com/ADVRHumanoids/xbot2_examples)

*Note:* the provided launch file accepts additional arguments to control the inclusions of perception sensors, namely `velodyne:=true`, and `realsense:=true`.
You need to have the proper dependencies installed in your setup in order for sensor simulation to work. See the [*forest recipe* for this package](https://github.com/ADVRHumanoids/multidof_recipes/blob/master/recipes/iit-centauro-ros-pkg.yaml).

How to create the Robot Model
=============================
*Note:* the repository contains generated files (urdf, srdf) so that is is ready to use without any generation step. The following instructions are meant for developers willing to modify the robot model.

First, install all required dependencies via the [`hhcm-forest` tool](https://github.com/ADVRHumanoids/forest), from the [`multidof_recipes`](https://github.com/ADVRHumanoids/multidof_recipes) registry. 

Now we can generate the urdf/srdf files via cmake:
1) `mkdir build && cd build`
2) `cmake ..`
3) `make generate`  (generates all files marked with `ADD_TO_ALL TRUE` into the build tree - see the cmakelists files)
4) (optional) `make publish` (publishes generated files to the source tree)
5) (optional) `make install` installs the source tree 
6) (optional) `make package` creates a `.deb` package from the source tree
