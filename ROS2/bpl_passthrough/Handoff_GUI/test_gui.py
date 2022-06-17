import sys
from std_msgs.msg import String, Float32MultiArray
import threading
from functools import partial

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow

import rclpy
from rcl_interfaces.msg import SetParametersResult
from rclpy.parameter import Parameter
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node



class GuiNode(Node):
	def __init__(self):
		super().__init__("simple_gui_node")
		self.counter_    = 0
		
		self.gui 			= None
		self.joint_IDs 		= None
		self.joint_names 	= None

		self.button_publisher_  = self.create_publisher(String, '/handoff_gui/button_presses', 10)

	def add_gui(self, gui):
		self.gui = gui

	def button_callback_(self, params, buttonPress=None):

		self.counter_ = self.counter_ + 1
		msg = String()

		if 	buttonPress	== "ba_o":
			msg.data = "A_OPEN"
		elif buttonPress	==  "ba_c":
			msg.data = "A_CLOSE"
		elif buttonPress	==  "bb_o":
			msg.data = "B_OPEN"
		elif buttonPress	==  "bb_c":
			msg.data = "B_CLOSE"
		else:
			pass

		print("Published: {}".format(msg.data))
		self.button_publisher_.publish(msg)

		return SetParametersResult(successful=True)

	def subscriber_callback_(self, msg):
		self.get_logger().info("Button clicked, " + msg.data)

class gui_handler():

	def __init__(self, ros_node, arm_name, joints):

		gui = QWidget()
		gui.setWindowTitle("Test Handoff GUI")
		gui.setGeometry(100, 100, 400, 800)

		buttonFrame = QHBoxLayout()
		
		buttons_A 			= QVBoxLayout()
		bravoA_btn_open 	= QPushButton('Bravo A OPEN')
		bravoA_btn_close 	= QPushButton('Bravo A CLOSE')
		buttons_A.addWidget(bravoA_btn_open)
		buttons_A.addWidget(bravoA_btn_close)
		bravoA_btn_open.clicked.connect(partial(ros_node.button_callback_, buttonPress="ba_o"))
		bravoA_btn_close.clicked.connect(partial(ros_node.button_callback_, buttonPress="ba_c"))
		buttonFrame.addLayout(buttons_A)

		"""
		buttons_B 			= QVBoxLayout()
		bravoB_btn_open 	= QPushButton('Bravo B OPEN')
		bravoB_btn_close 	= QPushButton('Bravo B CLOSE')
		buttons_B.addWidget(bravoB_btn_open)
		buttons_B.addWidget(bravoB_btn_close)
		bravoB_btn_open.clicked.connect(partial(ros_node.button_callback_, buttonPress="bb_o"))
		bravoB_btn_close.clicked.connect(partial(ros_node.button_callback_, buttonPress="bb_c"))
		buttonFrame.addLayout(buttons_B)
		"""

		gui.setLayout(buttonFrame)

		self.gui 				= gui
		self.bravoA_btn_open	= bravoA_btn_open
		self.bravoA_btn_close	= bravoA_btn_close
		self.bravoB_btn_open	= bravoB_btn_open
		self.bravoB_btn_close 	= bravoB_btn_close 	

	def get_gui(self):
		return self.gui

def main(args=None):



	rclpy.init(args=args)
	gui_app = QApplication(sys.argv)

	ros_node = GuiNode()
	gui_class = gui_handler(ros_node)
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

