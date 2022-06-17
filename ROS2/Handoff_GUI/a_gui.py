import sys
from std_msgs.msg import String, Float32MultiArray
import threading
from functools import partial

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow
from PyQt5 import QtCore

import rclpy
from rcl_interfaces.msg import SetParametersResult
from rclpy.parameter import Parameter
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node



bravo_7_arm_name		= "Bravo_A"
bravo_7_joint_names 	= ['bravo_axis_a', 'bravo_axis_b', 'bravo_axis_c', 'bravo_axis_d', 'bravo_axis_e', 'bravo_axis_f', 'bravo_axis_g']
bravo_7_joint_ids 		= [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]

bravo_5_arm_name		= "Bravo_B"
bravo_5_joint_names 	= ['bravo_axis_a', 'bravo_axis_b', 'bravo_axis_c', 'bravo_axis_d', 'bravo_axis_e']
bravo_5_joint_ids 		= [0x01, 0x02, 0x03, 0x04, 0x05]

#Running the 'a' py file
arm_name 		= bravo_7_arm_name
joint_names 	= bravo_7_joint_names
joint_ids 		= bravo_7_joint_ids
topic_name 		= '/handoff_gui/a_button_presses'

# Running the 'b' py file
#arm_name 		= bravo_5_arm_name
#joint_names 	= bravo_5_joint_names
#joint_ids 		= bravo_5_joint_ids
#topic_name 	= '/handoff_gui/b_button_presses'


class GuiNode(Node):
	def __init__(self):
		super().__init__("simple_gui_node")
		self.counter_    = 0
		
		self.gui 			= None
		self.joint_IDs 		= None
		self.joint_names 	= None

		self.button_publisher_  = self.create_publisher(Float32MultiArray, topic_name, 10)

	def add_gui(self, gui):
		self.gui = gui

	def button_callback_(self, params, info=None, buttonPress=None):

		self.counter_ = self.counter_ + 1
		msg = Float32MultiArray()
		
		base_vel = 0.01
		val = float("NAN")
		if 	buttonPress		== "+":
			val = base_vel
		elif buttonPress	== "-":
			val = -base_vel
		elif buttonPress	== "!":
			val = 0.0
		else:
			pass

		data = []
		for joint_name in joint_names:
			if joint_name != info['joint_name']:
				data.append(float("0.0"))
			else:
				data.append(val)
		msg.data = data
		print("Published: {}".format(data))
		self.button_publisher_.publish(msg)

		return SetParametersResult(successful=True)

	def subscriber_callback_(self, msg):
		self.get_logger().info("Button clicked, " + msg.data)

class gui_handler():

	def __init__(self, ros_node, arm_name, joint_names, joint_ids):

		gui = QWidget()
		gui.setWindowTitle("{} - Test Handoff GUI".format(arm_name))
		gui.setGeometry(100, 100, 200, 300)

		ui_frame = QVBoxLayout()
		lbl_arm_name = QLabel("<h1>{}</h1>".format(arm_name))
		lbl_arm_name.setAlignment(QtCore.Qt.AlignCenter)
		ui_frame.addWidget(lbl_arm_name)

		joint_frames = []
		for joint_name, joint_id in zip(joint_names, joint_ids):

			button_frame = QHBoxLayout()
			label_frame = QHBoxLayout()

			btn_minus 	= QPushButton('+')
			btn_plus 	= QPushButton('-')
			btn_stop	= QPushButton('Stop')
			lbl_joint 	= QLabel("{}\n({})".format(joint_name, joint_id))
			lbl_joint.setAlignment(QtCore.Qt.AlignCenter)

			buttonInfo = {'arm_name': arm_name, 'joint_name': joint_name, 'joint_id' : joint_id}
			btn_minus.clicked.connect(partial(ros_node.button_callback_, info= buttonInfo, buttonPress="+"))
			btn_plus.clicked.connect(partial(ros_node.button_callback_, info= buttonInfo, buttonPress="-"))
			btn_stop.clicked.connect(partial(ros_node.button_callback_, info= buttonInfo, buttonPress="!"))

			
			label_frame.addWidget(lbl_joint)

			button_frame.addWidget(btn_plus)
			button_frame.addWidget(btn_stop)
			button_frame.addWidget(btn_minus)

			
			#button_frame.addLayout(label_frame)
			joint_frames.append(label_frame)
			joint_frames.append(button_frame)

		for frame in joint_frames:
			ui_frame.addLayout(frame)

		gui.setLayout(ui_frame)

		self.gui = gui

	def get_gui(self):
		return self.gui

def main(args=None):

	rclpy.init(args=args)
	gui_app = QApplication(sys.argv)

	ros_node = GuiNode()
	gui_class = gui_handler(ros_node, arm_name, joint_names, joint_ids)
	gui = gui_class.get_gui()
	ros_node.add_gui(gui)

	executor = MultiThreadedExecutor() 
	executor.add_node(ros_node)
	new_thread = threading.Thread(target=executor.spin)

	try: 
		gui.show()
		new_thread.start()
		sys.exit(gui_app.exec())
	finally:
		#Will catch the sys.exit when gui.exec is closed, or any other exception, and clean up
		ros_node.get_logger().info("Shutting down")
		executor.shutdown()
		ros_node.destroy_node()

if __name__ == '__main__':
	main()     

