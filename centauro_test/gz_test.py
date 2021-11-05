from re import sub
import unittest
import subprocess
from os import path
from gazebo_msgs.srv import GetModelState
from std_srvs.srv import SetBool
import rospy
import time
import signal
import warnings

warnings.simplefilter("ignore", ResourceWarning)

class GzTest(unittest.TestCase):

    def setUp(self) -> None:

        self.gz = None
        self.xb = None

        this_dir = path.abspath(path.dirname(__file__))
        self.config_path = path.join(this_dir, '..', 'centauro_config', 'centauro_basic.yaml')

        self.get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        self.homing = rospy.ServiceProxy('/xbotcore/homing/switch', SetBool)

    def tearDown(self) -> None:
        self.get_model_state.close()

    def _wait_gz(self):
        timeout = 10
        
        try:
            self.get_model_state.wait_for_service(timeout=timeout)
            print('service active')
            time.sleep(1)
        except rospy.ROSException as e:
            print(f'timeout: {e}; exit status {self.gz.poll()}')
            return False 
            
        t0 = time.time()
        while time.time()  - t0 < timeout:
            res = self.get_model_state('centauro', '')
            if res.success:
                print('got centauro!')
                return True 
            else:
                print('centauro not spawned, retrying..')
                time.sleep(1)

        return False

    def _homing(self):
        timeout = 10
        self.homing.wait_for_service(timeout=timeout)
        print('homing available')
        time.sleep(1)
        return self.homing(True).success

    def _joint_state(self):
        from xbot_msgs.msg import JointState
        timeout = 10
        msg = rospy.wait_for_message('/xbotcore/joint_states', JointState, timeout=timeout)
        self.assertEqual(len(msg.name), 42)

    def _launch_gz(self, realsense=False, velodyne=False):
        proc = subprocess.Popen(
            args=['roslaunch', 
                  'centauro_gazebo', 
                  'centauro_world.launch', 
                  'gui:=false', f'realsense:={realsense}', f'velodyne:={velodyne}'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        return proc

    def _launch_xbot2(self):
        proc = subprocess.Popen(
            args=['xbot2-core', '--simtime', '--config', self.config_path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return proc

    def test_launch_gz_xbot2(self):
        
        warnings.simplefilter("ignore", ResourceWarning)
        warnings.simplefilter("ignore", DeprecationWarning)

        print('launching gz..')
        self.gz = self._launch_gz()
        print('gz running')
        
        self.assertTrue(self._wait_gz())

        print('launching xbot2')
        self.xb = self._launch_xbot2()
        print('xbot2 running')

        print('checking homing can be activated')
        self.assertTrue(self._homing())

        print('checking joint_states can be received')
        self._joint_state()

        self.xb.send_signal(signal.SIGINT)
        self.xb.wait()
        print('xbot2 closed')

        self.gz.send_signal(signal.SIGINT)
        self.gz.wait()
        print('gz closed')




if __name__ == '__main__':
    rospy.init_node('centauro_test_node')
    unittest.main()