import threading
import curses
import socket
import json
import sqlite3
import time
import queue

TCP_IP = '192.168.1.2'
TCP_PORT = 23
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

class Application:
	def __init__ (self):
		self.command = None
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.lastData = None

	def receiver(self):
		self.s.connect((TCP_IP, TCP_PORT))
		self.s.send(MESSAGE)	

		while True:
			self.lastData = self.s.recv(BUFFER_SIZE)
			if self.command != None and self.command == 'quit':
				return

	def commands(self):
		conn = sqlite3.connect('solarPanel.db')
		cursor = conn.cursor()	

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
					conn.commit()
					self.lastData = None
				except ValueError as e:
					break

			if self.command != None:
				if self.command == 'quit':
					self.s.close()
					conn.close()
					return
				elif self.command == 'create':
					cursor.execute("""CREATE TABLE voltages (
					timeRecorded integer,
					voltage_1 real,
					voltage_2 real,
					voltage_3 real,
					voltage_4 real
					)""")
					conn.commit()
				elif self.command == 'select':
					cursor.execute("SELECT * FROM voltages")
					ret = cursor.fetchall()
					for i in ret:
						print i
					conn.commit()
				elif self.command == 'delete':
					cursor.execute("DELETE FROM voltages")
					conn.commit()
				self.command = None

	def inputting(self):
	    while True:
	        if self.command == None:
	            self.command = raw_input("Enter a command: ")
            	if self.command == 'quit':
	        		return

	def run(self):
		t1 = threading.Thread(target=self.receiver, args=())
		t2 = threading.Thread(target=self.inputting, args=())
		t3 = threading.Thread(target=self.commands, args=())
		t1.start()
		t2.start()
		t3.start()
		t1.join()
		t2.join()
		t3.join()

if __name__ == "__main__":
	a = Application()
	a.run()