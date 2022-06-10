# Makind this for the bravo 7 for now.


import rclpy
from rclpy.node import Node

from bpl_msgs.msg import Packet

from bplprotocol import PacketReader, BPLProtocol, PacketID
import serial
import time

from sensor_msgs.msg import JointState


# Example multi joint status msg
"""
---
header:
  stamp:
    sec: 1654850290
    nanosec: 279750012
  frame_id: ''
name:
- bravo_axis_g
- bravo_axis_f
- bravo_axis_e
- bravo_axis_d
- bravo_axis_c
- bravo_axis_b
- bravo_axis_a
- bravo_finger_jaws_rs2_300_joint
- bravo_finger_jaws_rs2_301_joint
position:
- 0.0
- 2.6464
- 3.2
- 0.0
- 1.26272
- 0.0
- 0.0
- 0.0
- 0.0
velocity: []
effort: []
---

"""
# http://docs.ros.org/en/melodic/api/control_msgs/html/index-msg.html




class BPLControlNode(Node):

    def __init__(self):
        super().__init__("bpl_control_node")

        self.joints = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]
        self.frequency = 5
        self.packet_ids = [PacketID.POSITION, PacketID.VELOCITY]

        self.joint_names = ['bravo_axis_a', 'bravo_axis_b', 'bravo_axis_c', 'bravo_axis_d', 'bravo_axis_e', 'bravo_axis_f', 'bravo_axis_g']

        self.joint_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        self.tx_publisher = self.create_publisher(Packet, "tx", 10)
        self.joint_state_publisher = self.create_publisher(JointState, "joint_states", 10)

        self.rx_subscriber = self.create_subscription(Packet, "rx", self.request_handler, 10)

        self.request_packet = Packet()
        self.request_packet.device_id = 0xFF
        self.request_packet.packet_id = int(PacketID.REQUEST)
        self.request_packet.data = self.packet_ids

        self.timer = self.create_timer(1/self.frequency, self.request_data)
        self.timer2 = self.create_timer(1/20, self.publish_joint_state)


    def request_data(self):
        self.tx_publisher.publish(self.request_packet)

    def publish_joint_state(self):
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = self.joint_names
        joint_state.position = self.joint_positions.copy()
        self.joint_state_publisher.publish(joint_state)
        # print("send")

    def request_handler(self, packet):
        device_id = packet.device_id
        packet_id = packet.packet_id
        data = bytearray(packet.data)

        if packet_id == PacketID.POSITION:
            if device_id in self.joints:

                device_index = self.joints.index(device_id)
                
                position = BPLProtocol.decode_floats(data)[0]

                self.joint_positions[device_index] = position
                if device_id == 0x05:
                    print("Position Received: {} - {}".format(device_id, position)) 


def main(args=None):
    rclpy.init(args=args)
    jre = BPLControlNode()
    rclpy.spin(jre)


if __name__ == "__main__":
    main()