#!/usr/bin/env python

import xbot_interface.config_options as co
import xbot_interface.xbot_interface as xb
import numpy as np
import rospy


def move_to_q(robot, q0, q1, time):

    current_time = 0.0
    dt = 0.01

    while current_time <= time:
        alpha = current_time/time
        alpha = alpha**2*(2-alpha)**2
        q = alpha*q1 + (1-alpha)*q0
        robot.setPositionReference(q)
        robot.move()
        rospy.sleep(rospy.Duration(dt))
        current_time += dt


def fl_to_robot(robot, q, fl_q, signs=[-1, 1, -1]):

    fl_idx = robot.getDofIndex('hip_yaw_1')
    fr_idx = robot.getDofIndex('hip_yaw_2')
    rl_idx = robot.getDofIndex('hip_yaw_3')
    rr_idx = robot.getDofIndex('hip_yaw_4')

    fr_q = signs[0]*fl_q
    rl_q = signs[1]*fl_q
    rr_q = signs[2]*fl_q

    q1 = np.array(q)
    q1[fl_idx:(fl_idx + 6)] = fl_q
    q1[fr_idx:(fr_idx + 6)] = fr_q
    q1[rl_idx:(rl_idx + 6)] = rl_q
    q1[rr_idx:(rr_idx + 6)] = rr_q

    return q1

def get_robot():
    cfg = co.ConfigOptions()
    prefix = 'xbotcore/'
    urdf = rospy.get_param(prefix + 'robot_description')
    srdf = rospy.get_param(prefix + 'robot_description_semantic')

    cfg = co.ConfigOptions()
    cfg.set_urdf(urdf)
    cfg.set_srdf(srdf)
    cfg.generate_jidmap()
    cfg.set_string_parameter('framework', 'ROS')
    cfg.set_string_parameter('model_type', 'RBDL')
    cfg.set_bool_parameter('is_model_floating_base', True)
    robot = xb.RobotInterface(cfg)
    robot.sense()
    robot.setControlMode(xb.ControlMode.Position())
    robot.setControlMode({'j_wheel_1': xb.ControlMode.Velocity(),
                          'j_wheel_2': xb.ControlMode.Velocity(),
                          'j_wheel_3': xb.ControlMode.Velocity(),
                          'j_wheel_4': xb.ControlMode.Velocity()})
    return robot

def main():

    rospy.init_node('centauro_stress_test')

    time = 2.5

    robot = get_robot()


    # Rise arms and send them to the back
    q1 = robot.getPositionReference()
    # la_idx = robot.getDofIndex('j_arm1_1')
    # ra_idx = robot.getDofIndex('j_arm2_1')
    
    # q0 = np.array(q1)
    # la_q = np.array([1.45,  0.5, 0.0, -0.3, 0.0, 0.0])
    # ra_q = np.array([1.45, -0.5, 0.0, -0.3, 0.0, 0.0])
    # q1[la_idx:(la_idx + 6)] = la_q
    # q1[ra_idx:(ra_idx + 6)] = ra_q
    # move_to_q(robot, q0, q1, time)
    
    # q0 = np.array(q1)
    # la_q = np.array([1.45,  0.3, -1.7, -0.3, 0.0, 0.0])
    # ra_q = np.array([1.45, -0.3,  1.7, -0.3, 0.0, 0.0])
    # q1[la_idx:(la_idx + 6)] = la_q
    # q1[ra_idx:(ra_idx + 6)] = ra_q
    # move_to_q(robot, q0, q1, time)

    # q0 = np.array(q1)
    # la_q = np.array([1.45, 0.3, -1.7, -1.4, 0.0, 0.0])
    # ra_q = np.array([1.45, -0.3, 1.7, -1.4, 0.0, 0.0])
    # q1[la_idx:(la_idx + 6)] = la_q
    # q1[ra_idx:(ra_idx + 6)] = ra_q
    # move_to_q(robot, q0, q1, time)

    # Define joint velocity vector with 1 rad/s to all wheels
    wheel1_id = robot.getDofIndex('j_wheel_1')
    wheel2_id = robot.getDofIndex('j_wheel_2')
    wheel3_id = robot.getDofIndex('j_wheel_3')
    wheel4_id = robot.getDofIndex('j_wheel_4')

    qdot_ones = np.zeros_like(q1)
    qdot_ones[wheel1_id] = 1.0
    qdot_ones[wheel2_id] = 1.0
    qdot_ones[wheel3_id] = 1.0
    qdot_ones[wheel4_id] = 1.0

    niter = 1
    t0 = rospy.Time.now()

    while not rospy.is_shutdown():

        print('Started loop ', niter, ', elapsed time ', (rospy.Time.now() - t0).to_sec())
        niter += 1

        robot.setVelocityReference(qdot_ones * 2.0)

        q0 = np.array(q1)
        fl_q = np.array([0.0, -1.7, -2.3, 0.0, 1.5, 0.0])
        q1 = fl_to_robot(robot, q0, fl_q)
        move_to_q(robot, q0, q1, time)

        robot.setVelocityReference(qdot_ones * -2.0)

        q0 = np.array(q1)
        fl_q = np.array([0.0, 1.7, 2.3, 0.0, -1.5, 0.0])
        q1 = fl_to_robot(robot, q0, fl_q)
        move_to_q(robot, q0, q1, time)

        robot.setVelocityReference(qdot_ones * 2.0)

        q0 = np.array(q1)
        fl_q = np.array([0.0, -0.8, -0.8, 0.0, 1.5, 0.0])
        q1 = fl_to_robot(robot, q0, fl_q)
        move_to_q(robot, q0, q1, time)

        robot.setVelocityReference(qdot_ones * -2.0)

        q0 = np.array(q1)
        fl_q = np.array([-1.7, -0.8, -0.8, -2.0, -1.5, 0.0])
        q1 = fl_to_robot(robot, q0, fl_q, [1, 1, 1])
        move_to_q(robot, q0, q1, time)

        robot.setVelocityReference(qdot_ones * 2.0)

        q0 = np.array(q1)
        fl_q = np.array([0.2, -0.8, -0.8, 2.0, 1.5, 0.0])
        q1 = fl_to_robot(robot, q0, fl_q, [1, 1, 1])
        move_to_q(robot, q0, q1, time)

    # print('Bringing arms to the front..')

    # q0 = np.array(q1)
    # la_q = np.array([1.45, 0.3, -1.7, -1.4, 0.0, 0.0])
    # ra_q = np.array([1.45, -0.3, 1.7, -1.4, 0.0, 0.0])
    # q1[la_idx:(la_idx + 6)] = la_q
    # q1[ra_idx:(ra_idx + 6)] = ra_q
    # move_to_q(robot, q0, q1, time)

    # q0 = np.array(q1)
    # la_q = np.array([1.45, 0.3, -1.7, -0.3, 0.0, 0.0])
    # ra_q = np.array([1.45, -0.3, 1.7, -0.3, 0.0, 0.0])
    # q1[la_idx:(la_idx + 6)] = la_q
    # q1[ra_idx:(ra_idx + 6)] = ra_q
    # move_to_q(robot, q0, q1, time)

    # q0 = np.array(q1)
    # la_q = np.array([1.45, 0.5, 0.0, -0.3, 0.0, 0.0])
    # ra_q = np.array([1.45, -0.5, 0.0, -0.3, 0.0, 0.0])
    # q1[la_idx:(la_idx + 6)] = la_q
    # q1[ra_idx:(ra_idx + 6)] = ra_q
    # move_to_q(robot, q0, q1, time)

    print('Exiting..')


if __name__ == '__main__':
    main()