# iit-centauro-ros-pkg
Repository dedicated to the IIT robot CENTAURO

How to create the Robot Model:
==============================
To create the ```urdf```, ```srdf``` and ```sdf``` files go in:

```~/advr-superbuild/robots/iit-centauro-ros-pkg/centauro_urdf/script```

and run:

```./create_urdf_srdf_sdf.sh centauro```

Sticks:
-------
To use the sticks, go in:

```~/advr-superbuild/robots/iit-centauro-ros-pkg/centauro_urdf/urdf/config```

open the ```centauro.urdf.xacro``` file, set:

```<xacro:property name="USE_STICKS" value="true" />```

and create again the model files.
