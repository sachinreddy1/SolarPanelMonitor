from Globs import *

class Connection:
	def __init__ (self, socket, ip, port, connected):
		self.socket = socket
		self.ip = ip
		self.port = port
		self.connected = connected

		self.voltageValue = DEFAULT_VOLTAGE_THRES
		self.currentValue = DEFAULT_CURRENT_THRES
		self.temperatureValue = DEFAULT_TEMPERATURE_THRES
		self.configSwitch = 0
		self.manualSwitch = 0
