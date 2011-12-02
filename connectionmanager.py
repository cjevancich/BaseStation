import time
import struct
import settings

from PyQt4 import QtCore, QtGui, QtNetwork

class UdpClient(QtNetwork.QUdpSocket):
	def __init__(self):
		super(UdpClient, self).__init__()
	
	def setDestination(self, hostname, port):
		self.hostname = hostname
		self.bind()
		self.connectToHost(hostname, port)

	def sendData(self, data):
		if self.isValid():
			sent = self.write(data)
			if sent == -1:
				print 'Error code ', self.error()

class ControlGw(UdpClient):
	command_id = settings.ControlGw.command_id
	response_id = settings.ControlGw.response_id

	latencyUpdate = QtCore.pyqtSignal()
	connectionActive = QtCore.pyqtSignal()

	def __init__(self):
		super(ControlGw, self).__init__()
		self.readyRead.connect(self.handle_read)

		# setup ping timer
		self.ping_timer = QtCore.QTimer(self)
		self.ping_timer.setInterval(1000)
		self.ping_timer.setSingleShot(False)
		self.ping_timer.timeout.connect(self.do_ping)
		self.ping_timer.start()

		self.connected.connect(self.handle_connected)

	def sendCommand(self, command_id, data):
		msg = struct.pack('B', command_id)
		msg += data
		self.sendData(msg)

	def do_ping(self):
		if self.isValid():
			self.sendCommand(self.command_id['Ping'], struct.pack('d', time.time()*100))

	def handle_read(self):
		datagram, host, port = self.readDatagram(4096)
		cmd_id = ord(datagram[0])
		if cmd_id == self.response_id['Pong']:
			data = datagram[1:]
			if data == 'Connecting':
				self.connectionActive.emit()
			else:
				timeval = struct.unpack('d', data)[0] / 100.0
				latency = time.time() - timeval
				print 'latency is %f' % latency

	def handle_connected(self):
		self.sendCommand(self.command_id['Ping'], 'Connecting')

class StatePublisher(UdpClient):
	def __init__(self):
		super(StatePublisher, self).__init__()
		self.subscriptions = []
		self.resub_timer = QtCore.QTimer(self)
		self.resub_timer.setInterval(500)
		self.resub_timer.setSingleShot(False)
		self.resub_timer.timeout.connect(self.resub_timeout)
		self.resub_timer.start()

	def subscribeTo(prefix, persistent=True):
		if persistent:
			self.subscriptions.append(prefix)
		self.sendData(prefix)

	def resub_timeout(self):
		data = ''
		for sub in self.subscriptions:
			data += sub + '\n'
		# remove trailing \n
		data = data[:-1]
		if len(data) > 0:
			self.sendData(data)

class ConnectionManager(QtCore.QObject):

	validConnection = QtCore.pyqtSignal()
	disconnected = QtCore.pyqtSignal()

	def __init__(self):
		super(ConnectionManager, self).__init__()

		self.timeout_secs = 10
		self.is_connected = False

	def connected(self):
		return self.is_connected

	def do_connect(self, host):
		if self.connected():
			self.do_disconnect()
		self.progress = QtGui.QProgressDialog("Connecting to quadcopter...", "Cancel", 0, 2)
		self.progress.canceled.connect(self.do_disconnect)
		self.progress.setVisible(True)
		self.progress.setValue(0)

		self.control_sock = ControlGw()
		self.control_sock.setDestination(host, 8091)
		self.control_sock.connectionActive.connect(self.handle_cgw_active)

		self.state_sock = StatePublisher()
		self.state_sock.setDestination(host, 8092)

		# We dont have a verify state connection method
		self.progress.setValue(1 + self.progress.value())

	def do_disconnect(self):
		try:
			del self.control_sock
		except AttributeError:
			pass
		try:
			del self.state_sock
		except AttributeError:
			pass
		self.is_connected = False
		self.disconnected.emit()


	def try_command(self, command_name, data):
		if not self.connected():
			return

		try:
			cmd_id = ControlGw.command_id[command_name]
		except KeyError:
			return

		self.control_sock.sendCommand(command_id, data)

	def handle_cgw_active(self):
		self.progress.setValue(self.progress.value() + 1)

