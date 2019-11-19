# DEFAULT THRESHOLD VALUES
DEFAULT_VOLTAGE_THRES = 36.0
DEFAULT_CURRENT_THRES = 0.75
DEFAULT_TEMPERATURE_THRES = 27.0

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
		self.power = 'ON'

