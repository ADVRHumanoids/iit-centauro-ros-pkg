#!/usr/bin/env python

from cartesian_interface.pyci_all import *
import rospy
import math
import numpy as np


def main():

    # obtain ci ros client
    ci = pyci.CartesianInterfaceRos()

    # define time between waypoints
    time = 3.0

    # forward velocity to base
    ci.setControlMode('pelvis', pyci.ControlType.Velocity)
    vref = np.array([0.05, 0, 0, 0, 0, 0])
    ci.setVelocityReferenceAsync('pelvis', vref, -1.0)  # timeout = -1.0 means 'forever'

    # update ci with latest values
    ci.update()

    # wide support
    print 'Wide support..'
    b_t_w = ci.getPoseReference('fl_wheel')[0]
    ci.setTargetPose('fl_wheel', Affine3(pos=[0.3, 0.45, b_t_w.translation[2]]), time)

    b_t_w = ci.getPoseReference('fr_wheel')[0]
    ci.setTargetPose('fr_wheel', Affine3(pos=[0.3, -0.45, b_t_w.translation[2]]), time)

    b_t_w = ci.getPoseReference('hl_wheel')[0]
    ci.setTargetPose('hl_wheel', Affine3(pos=[-0.3, 0.45, b_t_w.translation[2]]), time)

    b_t_w = ci.getPoseReference('hr_wheel')[0]
    ci.setTargetPose('hr_wheel', Affine3(pos=[-0.3, -0.45, b_t_w.translation[2]]), time)

    ci.waitReachCompleted('hr_wheel')
    rospy.sleep(1.0)

    # narrow support
    print 'Narrow support..'
    b_t_w = ci.getPoseReference('fl_wheel')[0]
    ci.setTargetPose('fl_wheel', Affine3(pos=[0.5, 0.25, b_t_w.translation[2]]), time)

    b_t_w = ci.getPoseReference('fr_wheel')[0]
    ci.setTargetPose('fr_wheel', Affine3(pos=[0.5, -0.25, b_t_w.translation[2]]), time)

    b_t_w = ci.getPoseReference('hl_wheel')[0]
    ci.setTargetPose('hl_wheel', Affine3(pos=[-0.5, 0.25, b_t_w.translation[2]]), time)

    b_t_w = ci.getPoseReference('hr_wheel')[0]
    ci.setTargetPose('hr_wheel', Affine3(pos=[-0.5, -0.25, b_t_w.translation[2]]), time)

    ci.waitReachCompleted('hr_wheel')
    rospy.sleep(1.0)

    # homing support
    print 'Homing support..'
    b_t_w = ci.getPoseReference('fl_wheel')[0]
    ci.setTargetPose('fl_wheel', Affine3(pos=[0.35, 0.35, b_t_w.translation[2]]), time)

    b_t_w = ci.getPoseReference('fr_wheel')[0]
    ci.setTargetPose('fr_wheel', Affine3(pos=[0.35, -0.35, b_t_w.translation[2]]), time)

    b_t_w = ci.getPoseReference('hl_wheel')[0]
    ci.setTargetPose('hl_wheel', Affine3(pos=[-0.35, 0.35, b_t_w.translation[2]]), time)

    b_t_w = ci.getPoseReference('hr_wheel')[0]
    ci.setTargetPose('hr_wheel', Affine3(pos=[-0.35, -0.35, b_t_w.translation[2]]), time)

    ci.waitReachCompleted('hr_wheel')
    rospy.sleep(1.0)

    # stop forward motion
    ci.setVelocityReferenceAsync('pelvis', [0, 0, 0, 0, 0, 0], 1.0)
    ci.setControlMode('pelvis', pyci.ControlType.Position)

    # go through waypoints with wheeled motion
    pelvis_pose_initial, _, _ = ci.getPoseReference('pelvis')  # initial pelvis pose
    pelvis_z = pelvis_pose_initial.translation[2]
    waypoints = []

    wp = pyci.WayPoint(Affine3(pos=[1.0, 0.0, 0.0])*pelvis_pose_initial, time)  # move forward
    waypoints.append(wp)

    wp = pyci.WayPoint(Affine3(pos=[1.0, 0.5, 0.0])*pelvis_pose_initial, 2*time)  # move left
    waypoints.append(wp)

    wp = pyci.WayPoint(Affine3(pos=[1.0, -0.5, 0.0])*pelvis_pose_initial, 3*time)  # move right
    waypoints.append(wp)

    wp = pyci.WayPoint(Affine3(pos=[1.0, -0.5, 0.0], rot=[0, 0, 1, 1])*pelvis_pose_initial, 5*time)  # move CCW
    waypoints.append(wp)

    wp = pyci.WayPoint(Affine3(pos=[1.0, -0.5, 0.0], rot=[0, 0, -1, 1])*pelvis_pose_initial, 7*time)  # move CW
    waypoints.append(wp)

    wp = pyci.WayPoint(pelvis_pose_initial, 10*time)  # move to initial pose
    waypoints.append(wp)

    ci.setWaypoints('pelvis', waypoints)
    ci.waitReachCompleted('pelvis')

    print 'Motion completed!'






if __name__ == '__main__':
    rospy.init_node('virtual_frame_test')
    main()
