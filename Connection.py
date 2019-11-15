class Connection:
	def __init__ (self, socket, ip, port, connected):
		self.socket = socket
		self.ip = ip
		self.port = port
		self.connected = connected

		self.voltageValue = None
		self.currentValue = None
		self.temperatureValue = None
		self.power = 'ON'

