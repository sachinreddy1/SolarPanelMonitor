import threading
import json
import sqlite3
import time
from Connector import *
from Monitor import *
from Connection import *

BUFFER_SIZE = 1024

class Application:
	def __init__ (self):
		self.lastData = None
		self.command = None
		self.monitor = None
		self.c = Connector()

	# ----------------- #

	def commands(self):
		self.conn = sqlite3.connect('solarPanel.db')
		cursor = self.conn.cursor()	
		
		# Check if table exists.
		cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='voltages' ''')
		if cursor.fetchone()[0] == 0:
			cursor.execute("""CREATE TABLE voltages (
			timeRecorded integer,
			voltage_1 real,
			voltage_2 real,
			voltage_3 real,
			current_1 real,
			temperature_1 real,
			temperature_2 real,
			temperature_3 real,
			temperature_4 real,
			temperature_5 real,
			temperature_6 real
			)""")	

		while True:
			if self.lastData:
				try:
					packet = json.loads(self.lastData)
					cursor.execute("INSERT INTO voltages VALUES (:timeRecorded, :voltage_1, :voltage_2, :voltage_3, :current_1, :temperature_1, :temperature_2, :temperature_3, :temperature_4, :temperature_5, :temperature_6)", 
					{
					'timeRecorded': time.time(), 
					'voltage_1': packet["V1"], 
					'voltage_2': packet["V2"], 
					'voltage_3': packet["V3"], 
					'current_1': packet["C1"],
					'temperature_1': packet["T1"],
					'temperature_2': packet["T2"],
					'temperature_3': packet["T3"],
					'temperature_4': packet["T4"],
					'temperature_5': packet["T5"],
					'temperature_6': packet["T6"]
					})
					self.conn.commit()
					self.lastData = None
				except ValueError as e:
					pass

			if self.command != None:
				if self.command == 'quit':
					self.conn.close()
					self.monitor.root.quit()
					for i in self.c.connections:
						i.socket.close()
					return					
				elif self.command == 'select':
					cursor.execute("SELECT * FROM voltages")
					ret = cursor.fetchall()
					self.monitor.label['text'] = self.formatSelect(ret)
					self.conn.commit()
				elif self.command == 'delete':
					cursor.execute("DELETE FROM voltages")
					self.conn.commit()
				elif self.command == 'sync':
					self.c.clear()
					self.monitor.clearWidgets()
					self.monitor.updateWidgets()
					self.c.connect()
					self.monitor.updateWidgets()

				self.command = None

	# ----------------- #

	def receiver(self):
		self.c.connect()
		self.monitor.updateWidgets()

		while True:
			for i in self.c.connections:
				if i.connected and self.command != 'sync' and self.command != 'quit':
					# SEND
					data = {}
					data['V'] = i.voltageValue
					data['C'] = i.currentValue
					data['T'] = i.temperatureValue
					data['S'] = i.configSwitch
					data['P'] = i.power
					i.socket.send(json.dumps(data))
					# RECEIVE
					self.lastData = i.socket.recv(BUFFER_SIZE)
					
			if self.command == 'quit':
				return

	# ----------------- #

	def inputting(self, command):
		self.command = command

	def thresholdInputting(self, voltageValue, currentValue, temperatureValue, i):
		if len(self.c.connections) == 0:
			return
		self.c.connections[i].voltageValue = voltageValue
		self.c.connections[i].currentValue = currentValue
		self.c.connections[i].temperatureValue = temperatureValue

	def configSwitchInputting(self, connection, i):
		if len(self.c.connections) == 0:
			return
		self.c.connections[connection].configSwitch = i

	def powerInputting(self, i):
		if len(self.c.connections) == 0:
			return
		if self.c.connections[i].power == 'ON':
			self.c.connections[i].power = 'OFF'
			self.monitor.togglePowerButton['text'] = 'ON'	#
		else:
			self.c.connections[i].power = 'ON'
			self.monitor.togglePowerButton['text'] = 'OFF'	#

	def formatSelect(self, input):
		ret = ""
		for i in input:
			ret += str(i) + "\n"
		return ret

	# ----------------- #

	def run(self, monitor):
		t1 = threading.Thread(target=self.receiver, args=())
		t2 = threading.Thread(target=self.commands, args=())
		t1.start()
		t2.start()
		self.monitor = monitor
		self.monitor.run()
		t1.join()
		t2.join()

if __name__ == "__main__":
	a = Application()
	m = Monitor(a)
	a.run(m)