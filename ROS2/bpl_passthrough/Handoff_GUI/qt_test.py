import sys
from functools import partial
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow

def test_func(params=None, buttonPress=None):
	print(buttonPress)
class gui_handler():

	def __init__(self):

		gui = QWidget()
		gui.setWindowTitle("Test Handoff GUI")
		gui.setGeometry(100, 100, 400, 800)

		buttonFrame = QHBoxLayout()
		
		buttons_A 			= QVBoxLayout()
		bravoA_btn_open 	= QPushButton('Bravo A OPEN')
		bravoA_btn_close 	= QPushButton('Bravo A CLOSE')
		buttons_A.addWidget(bravoA_btn_open)
		buttons_A.addWidget(bravoA_btn_close)
		bravoA_btn_open.clicked.connect(partial(test_func, buttonPress="ba_o"))
		bravoA_btn_close.clicked.connect(partial(test_func, buttonPress="ba_c"))
		buttonFrame.addLayout(buttons_A)

		buttons_B 			= QVBoxLayout()
		bravoB_btn_open 	= QPushButton('Bravo B OPEN')
		bravoB_btn_close 	= QPushButton('Bravo B CLOSE')
		buttons_B.addWidget(bravoB_btn_open)
		buttons_B.addWidget(bravoB_btn_close)
		bravoB_btn_open.clicked.connect(partial(test_func, buttonPress="bb_o"))
		bravoB_btn_close.clicked.connect(partial(test_func, buttonPress="bb_c"))
		buttonFrame.addLayout(buttons_B)

		gui.setLayout(buttonFrame)

		self.gui 				= gui
		self.bravoA_btn_open	= bravoA_btn_open
		self.bravoA_btn_close	= bravoA_btn_close
		self.bravoB_btn_open	= bravoB_btn_open
		self.bravoB_btn_close 	= bravoB_btn_close 

	def get_gui(self):
		return self.gui



try:
	gui_app = QApplication(sys.argv)
	gui_handler = gui_handler()

	gui_handler.get_gui().show()
	sys.exit(gui_app.exec())
finally:
	print("wack")