# user input should go in as metres! 
# ros2 topic pub "pose_string" std_msgs/String 'data: "0.2 -0.3 0.5"' --once

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String, Header
from builtin_interfaces.msg import Time

class BPLPoseControlPublisher(Node):
    
    def __init__(self):
        super().__init__("bpl_pose_control_published_node")

        #self.input_coords = [0.0, 0.0, 0.0]
        #self.output_pose = Pose()

        self.declare_parameter('request_frequency', 10)
        self.declare_parameter('publish_frequency', 10)

        self.request_frequency = self.get_parameter('request_frequency').value
        self.publish_frequency = self.get_parameter('publish_frequency').value

        # should I initialise this to something? 
        self.current_pose = PoseStamped()

        #self.pose_publisher = self.create_publisher(PoseStamped, "pose_control", 10)
        self.pose_publisher = self.create_publisher(PoseStamped, "command/km_command", 10)

        # subscribe to the user input 
        self.pose_str_subscriber = self.create_subscription(String, "pose_string", self.convert_input_to_pose, 10)
        # subscribe to the 
        self.km_end_pose_subscriber = self.create_subscription(PoseStamped, "current_pose", self.received_pose, 10)

    def publish_pose(self, pose):
        self.pose_publisher.publish(pose)
        self.get_logger().info(f'Published pose: {pose}')
   
    def convert_input_to_pose(self, input):
        self.get_logger().info(f'Received input string: {input}')
        input_list = []
        input_list = list(input.data.split())

        output_pose = PoseStamped()

        # Pose Position
        output_pose.pose.position.x = float(input_list[0])
        output_pose.pose.position.y = float(input_list[1])
        output_pose.pose.position.z = float(input_list[2])

        # Pose Orientation (Quaternion)
        if self.current_pose is not None:
            output_pose.pose.orientation = self.current_pose.pose.orientation
        else:
            output_pose.pose.orientation.x = 0.0
            output_pose.pose.orientation.y = 0.0
            output_pose.pose.orientation.z = 0.0
            output_pose.pose.orientation.w = 1.0

        output_pose.header = self.make_header()

        self.publish_pose(output_pose)
    
    def make_header(self):
        hdr = Header()
        hdr.frame_id = "base_link"
        hdr.stamp = self.get_clock().now().to_msg()
        return hdr
    
    def received_pose(self, pose):
        self.current_pose = pose


def main(args = None):
    rclpy.init(args=args)
    pcp = BPLPoseControlPublisher()
    rclpy.spin(pcp)

if __name__ == "__main__":
    main()
    