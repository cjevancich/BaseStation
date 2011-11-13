from PyQt4 import QtGui

import attenuationwidget

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.initUi()

	def initUi(self):
		self.setWindowTitle('Quadcopter BaseStation')

		exitAction = QtGui.QAction('&Exit', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(QtGui.qApp.quit)

		connectAction = QtGui.QAction('&Connect', self)
		connectAction.setStatusTip('Connect to the quadcopter')
		self.connectAction = connectAction

		disconnectAction = QtGui.QAction('&Disconnect', self)
		disconnectAction.setStatusTip('Disconnect from the quadcopter')
		self.disconnectAction = disconnectAction

		menubar = self.menuBar()
		fileMenu = menubar.addMenu("&File")
		fileMenu.addAction(connectAction)
		fileMenu.addAction(disconnectAction)
		fileMenu.addSeparator()
		fileMenu.addAction(exitAction)

		self.gyro_widget = attenuationwidget.AttenuationWidget()
		self.setCentralWidget(self.gyro_widget)

		self.on_disconnect()

	def on_disconnect(self):
		self.statusBar().showMessage("Disconnected.")
		self.disconnectAction.setEnabled(False)


	def on_connect(self):
		self.statusBar().showMessage("Connected.")
		self.connectAction.setEnabled(False)
