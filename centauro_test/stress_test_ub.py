#!/usr/bin/env python

import xbot_interface.config_options as cfg
import xbot_interface.xbot_interface as xb
import numpy as np
import rospy

from stress_test_lb import move_to_q, get_robot

def la_to_robot(robot, q, la_q, signs):

    la_idx = robot.getDofIndex('j_arm1_1')
    ra_idx = robot.getDofIndex('j_arm2_1')

    ra_q = la_q * signs

    q1 = np.array(q)
    q1[la_idx:(la_idx + 6)] = la_q[:6]
    q1[ra_idx:(ra_idx + 6)] = ra_q[:6]

    return q1


def main():
    rospy.init_node('centauro_stress_test')

    time = 3.0

    robot = get_robot()

    # Rise arms and send them to the back
    q1 = robot.getMotorPosition()

    s = np.array([1, -1, -1, 1, -1, 1, 1])

    niter = 1
    t0 = rospy.Time.now()

    while not rospy.is_shutdown():
        print('Started loop ', niter, ', elapsed time ', (rospy.Time.now() - t0).to_sec())
        niter += 1

        q0 = np.array(q1)
        la_q = np.array([0.6, 2.3, 0.0, 0.0, -2.4, -1.4, -2.0])
        q1 = la_to_robot(robot, q0, la_q, s)
        move_to_q(robot, q0, q1, time)

        q0 = np.array(q1)
        la_q = np.array([-3.0, 2.3, -2.3, 0.0, 2.4, 1.4, 2.0])
        q1 = la_to_robot(robot, q0, la_q, s)
        move_to_q(robot, q0, q1, time)

        q0 = np.array(q1)
        la_q = np.array([1.4, 0.1, 2.3, -2.3, -2.4, -1.4, -2.0])
        q1 = la_to_robot(robot, q0, la_q, s)
        move_to_q(robot, q0, q1, time)
        
        q0 = np.array(q1)
        la_q = np.array([0.6, 0.3, 0.0, -1.9, 0.0, -0.5, -2.0])
        q1 = la_to_robot(robot, q0, la_q, s)
        move_to_q(robot, q0, q1, time)


    # q0 = np.array(q1)
    # la_q = np.array([1.45, 0.3, -1.7, -1.4, 0.0, 0.0])
    # ra_q = np.array([1.45, -0.3, 1.7, -1.4, 0.0, 0.0])
    # q1[la_idx:(la_idx + 6)] = la_q
    # q1[ra_idx:(ra_idx + 6)] = ra_q
    # move_to_q(robot, q0, q1, time)
    #
    # q0 = np.array(q1)
    # la_q = np.array([1.45, 0.3, -1.7, -0.3, 0.0, 0.0])
    # ra_q = np.array([1.45, -0.3, 1.7, -0.3, 0.0, 0.0])
    # q1[la_idx:(la_idx + 6)] = la_q
    # q1[ra_idx:(ra_idx + 6)] = ra_q
    # move_to_q(robot, q0, q1, time)
    #
    # q0 = np.array(q1)
    # la_q = np.array([1.45, 0.5, 0.0, -0.3, 0.0, 0.0])
    # ra_q = np.array([1.45, -0.5, 0.0, -0.3, 0.0, 0.0])
    # q1[la_idx:(la_idx + 6)] = la_q
    # q1[ra_idx:(ra_idx + 6)] = ra_q
    # move_to_q(robot, q0, q1, time)

    print('Exiting..')


if __name__ == '__main__':
    main()