import socket
import json
import sqlite3
import time

TCP_IP = '192.168.1.2'
TCP_PORT = 23
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
# ----------- #
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
# ----------- #
conn = sqlite3.connect('solarPanel.db')
cursor = conn.cursor()

while 1:
	data = s.recv(BUFFER_SIZE)
	try:
		packet = json.loads(data)
		# print "voltage_1", packet["voltage_1"]
		# print "voltage_2", packet["voltage_2"]
		# print "voltage_3", packet["voltage_3"]
		# print "voltage_4", packet["voltage_4"]
		cursor.execute("INSERT INTO voltages VALUES (:timeRecorded, :voltage_1, :voltage_2, :voltage_3, :voltage_4)", 
			{
			'timeRecorded': time.time(), 
			'voltage_1': packet["voltage_1"], 
			'voltage_2': packet["voltage_2"], 
			'voltage_3': packet["voltage_3"], 
			'voltage_4': packet["voltage_4"]
			})
		conn.commit()
  	except ValueError as e:
		print "Unreliable data received."
	
s.close()
conn.close()
