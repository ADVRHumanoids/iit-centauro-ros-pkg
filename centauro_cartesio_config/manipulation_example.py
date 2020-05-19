#!/usr/bin/env python

from cartesian_interface.pyci_all import *
import rospy
import math
import numpy as np

# position:
#     x: 0.942016661167
#     y: 0.156102731824
#     z: 0.0738918185234
#   orientation:
#     x: 0.332115201177
#     y: -4.84459744084e-07
#     z: 0.603846665623
#     w: 0.724616241581
#
# position:
#     x: 0.942016661167
#     y: 0.156102731824
#     z: 0.0738918185234
#     orientation:z
# x: -0.811944454272
# y: -0.57146708015
# z: -0.118980969499
# w: 0.00388694982374
#
# position:
#     x: 1.03693151474
#     y: 0.22765211761
#     z: -0.590673923492
#   orientation:
#     x: 0.778994600312
#     y: 0.513390667734
#     z: 0.277779014501
#     w: 0.228989637476


def main():

    # obtain ci ros client
    ci = pyci.CartesianInterfaceRos()

    # define time between waypoints
    time = 3.0

    # go through waypoints with wheeled motion
    l_waypoints = []
    r_waypoints = []

    # left arm
    l_arm_start, _, _ = ci.getPoseReference('arm1_8')

    wp = pyci.WayPoint(Affine3(pos=[0.95, 0.15, 0.07],
                               rot=[0.33, 0.0, 0.60, 0.72]),
                       time)
    l_waypoints.append(wp)

    wp = pyci.WayPoint(Affine3(pos=[0.95, 0.15, 0.07],
                               rot=[-0.80, -0.60, -0.10, 0.0]),
                       2*time)
    l_waypoints.append(wp)

    wp = pyci.WayPoint(Affine3(pos=[1.0, 0.15, -0.50],
                               rot=[0.80, 0.60, 0.0, 0.0]),
                       3*time)
    l_waypoints.append(wp)

    wp = pyci.WayPoint(Affine3(pos=[0.95, 0.15, 0.07],
                               rot=[0.33, 0.0, 0.60, 0.72]),
                       4*time)
    l_waypoints.append(wp)

    l_waypoints.append(pyci.WayPoint(l_arm_start, 5*time))

    # right arm
    r_arm_start, _, _ = ci.getPoseReference('arm2_8')

    wp = pyci.WayPoint(Affine3(pos=[0.95, -0.15, 0.07],
                               rot=[0.0, 0.33, 0.72, 0.60]),
                       time)
    r_waypoints.append(wp)

    wp = pyci.WayPoint(Affine3(pos=[0.95, -0.15, 0.07],
                               rot=[-0.60, -0.80, 0.00, -0.10]),
                       2*time)
    r_waypoints.append(wp)

    wp = pyci.WayPoint(Affine3(pos=[1.0, -0.15, -0.50],
                               rot=[0.60, 0.80, 0.0, 0.0]),
                       3*time)
    r_waypoints.append(wp)

    wp = pyci.WayPoint(Affine3(pos=[0.95, -0.15, 0.07],
                               rot=[0.0, 0.33, 0.72, 0.60]),
                       4*time)
    r_waypoints.append(wp)

    r_waypoints.append(pyci.WayPoint(r_arm_start, 5*time))

    ci.setWaypoints('arm1_8', l_waypoints)
    ci.setWaypoints('arm2_8', r_waypoints)
    ci.waitReachCompleted('arm1_8')
    ci.waitReachCompleted('arm2_8')

    print 'Motion completed!'






if __name__ == '__main__':
    rospy.init_node('virtual_frame_test')
    main()
