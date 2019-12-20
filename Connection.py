from Globs import *

# Main class for connections
class Connection:
	def __init__ (self, socket, ip, port, connected):
		# Connection values
		self.socket = socket
		self.ip = ip
		self.port = port
		self.connected = connected

		# Values to configure
		self.voltageValue = DEFAULT_VOLTAGE_THRES
		self.currentValue = DEFAULT_CURRENT_THRES
		self.temperatureValue = DEFAULT_TEMPERATURE_THRES
		self.configSwitch = 0
		self.manualSwitch = 0

		self.currentAck = 0
