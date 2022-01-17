# iit-centauro-ros-pkg
Repository dedicated to the IIT robot CENTAURO

How to create the Robot Model:
==============================

*Note:* the repository contains generated files (urdf, srdf) so that is is ready to use without any generation step. The following instructions are meant for developers willing to modify the robot model.

1) `mkdir build && cd build`
2) `cmake ..`
3) `make`  (generates all files marked with `ADD_TO_ALL TRUE` into the build tree - see the cmakelists files)
4) (optional) `make publish_urdf_all publish_srdf_all` (publishes generated files to the source tree)
5) (optional) `make install` installs the source tree 
6) (optional) `make package` creates a `.deb` package from the source tree