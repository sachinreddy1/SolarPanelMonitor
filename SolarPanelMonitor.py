import threading
import json
import sqlite3
import time
from Connector import *
from Monitor import *

BUFFER_SIZE = 1024

class Application:
	def __init__ (self):
		self.lastData = None
		self.command = None
		self.monitor = None
		self.c = Connector()
		
		self.voltageValue = None
		self.currentValue = None
		self.power = 'ON'

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
			voltage_4 real
			)""")	

		while True:
			if self.lastData:
				try:
					packet = json.loads(self.lastData)
					cursor.execute("INSERT INTO voltages VALUES (:timeRecorded, :voltage_1, :voltage_2, :voltage_3, :voltage_4)", 
					{
					'timeRecorded': time.time(), 
					'voltage_1': packet["voltage_1"], 
					'voltage_2': packet["voltage_2"], 
					'voltage_3': packet["voltage_3"], 
					'voltage_4': packet["voltage_4"]
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
				if i.connected:
					# SEND
					data = {}
					data['V'] = self.voltageValue
					data['C'] = self.currentValue
					data['P'] = self.power
					i.socket.send(json.dumps(data))
					# RECEIVE
					self.lastData = i.socket.recv(BUFFER_SIZE)
					
			if self.command == 'quit':
				return

	# ----------------- #

	def inputting(self, command):
		self.command = command

	def thresholdInputting(self, voltageValue, currentValue):
		self.voltageValue = voltageValue
		self.currentValue = currentValue

	def powerInputting(self):
		if self.power == 'ON':
			self.power = 'OFF'
			self.monitor.togglePowerButton['text'] = 'ON'
		else:
			self.power = 'ON'
			self.monitor.togglePowerButton['text'] = 'OFF'

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