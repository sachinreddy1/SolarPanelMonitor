class Connection:
	def __init__ (self, socket, ip, connected):
		self.socket = socket
		self.ip = ip
		self.connected = connected