#!/usr/bin/env python3
"""
Republishes a sensor_msgs/CameraInfo message with a remapped frame_id.
Parameters:
  input_topic  (str)  – topic to subscribe to   [default: 'camera_info_in']
  output_topic (str)  – topic to publish on      [default: 'camera_info_out']
  frame_id     (str)  – frame_id to inject        [default: 'camera_optical_frame']
  qos_depth    (int)  – history depth for both sub and pub [default: 1]
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from sensor_msgs.msg import CameraInfo


class CameraInfoFrameRemapper(Node):

    def __init__(self) -> None:
        super().__init__('camera_info_frame_remapper')

        # ── declare & read parameters ────────────────────────────────────────
        self.declare_parameter('input_topic',  'camera_info_in')
        self.declare_parameter('output_topic', 'camera_info_out')
        self.declare_parameter('frame_id',     'camera_optical_frame')
        self.declare_parameter('qos_depth',    1)

        input_topic  = self.get_parameter('input_topic').value
        output_topic = self.get_parameter('output_topic').value
        self._frame_id = self.get_parameter('frame_id').value
        qos_depth    = self.get_parameter('qos_depth').value

        # ── QoS: best-effort, keep-last(depth) ──────────────────────────────
        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=qos_depth,
        )

        # ── publisher first so it is ready before the first callback ────────
        self._pub = self.create_publisher(CameraInfo, output_topic, qos)

        self._sub = self.create_subscription(
            CameraInfo,
            input_topic,
            self._callback,
            qos,
        )

        self.get_logger().info(
            f"Remapping '{input_topic}' → '{output_topic}' "
            f"with frame_id='{self._frame_id}'"
        )

    # ── hot path: mutate in-place and republish ──────────────────────────────
    def _callback(self, msg: CameraInfo) -> None:
        msg.header.frame_id = self._frame_id
        self._pub.publish(msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = CameraInfoFrameRemapper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
