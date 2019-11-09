import threading
import curses
import socket
import json
import sqlite3
import time
import queue
import tkinter as tk
from tkinter import ttk
import signal

import select

_TCP_IP = '192.168.1.6'
TCP_IP = '192.168.1.4'
TCP_PORT = 23
BUFFER_SIZE = 1024

HEIGHT = 500
WIDTH = 600

class Application:
	def __init__ (self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#
		self.lastData = None
		#
		self.root = None
		#
		self.connected = False
		#
		self.command = None
		#
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
					self.s.close()
					self.conn.close()
					self.root.quit()
					return					
				elif self.command == 'select':
					cursor.execute("SELECT * FROM voltages")
					ret = cursor.fetchall()
					self.label['text'] = self.formatSelect(ret)
					self.conn.commit()
				elif self.command == 'delete':
					cursor.execute("DELETE FROM voltages")
					self.conn.commit()
				elif self.command == 'status':
					self.label['text'] = "TRUE" if self.connected else "FALSE"
				elif self.command == 'sync' and not self.connected:
					self.s.settimeout(5)
					self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					try:
						self.s.connect((TCP_IP, TCP_PORT))
						self.connected = True
						# Setting color
						self.ipLabel['text'] = 'IP: ' + TCP_IP
						self.ipStatus['text'] = 'Status: Connected'
						self.ipStatus.config(fg="#32cd32")
					except:
						self.connected = False

				self.command = None

	# ----------------- #

	def receiver(self):

		# Check for a connection
		self.s.settimeout(5)
		try:
			self.s.connect((_TCP_IP, TCP_PORT))
			self.connected = True
		except:
			self.connected = False
		
		while True:
			if self.connected:
				# SEND
				data = {}
				data['V'] = self.voltageValue
				data['C'] = self.currentValue
				data['P'] = self.power
				self.s.send(json.dumps(data))
				# RECEIVE
				self.lastData = self.s.recv(BUFFER_SIZE)
				
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
			self.togglePowerButton['text'] = 'ON'
		else:
			self.power = 'ON'
			self.togglePowerButton['text'] = 'OFF'

	# ----------------- #

	def formatSelect(self, input):
		ret = ""
		for i in input:
			ret += str(i) + "\n"
		return ret

	# ----------------- #

	def monitor(self):
		self.root = tk.Tk()
		
		# Main window
		self.root.winfo_toplevel().title("Solar Panel Monitor")
		self.root.geometry('{}x{}'.format(WIDTH, HEIGHT))
		self.root.configure(bg='#383735')

		# Top frame - Debug for commands
		frame = tk.Frame(self.root, bg='#383735')
		frame.place(relx=0.5, rely=0.05, relwidth=0.75, relheight=0.1, anchor='n')

		entry = tk.Entry(frame, font=40)
		entry.place(relwidth=0.65, relheight=0.5)

		button = tk.Button(frame, text="Command", font=40, command=lambda: self.inputting(entry.get()))
		button.place(relx=0.7, relwidth=0.3, relheight=0.5)

		# ----------------- #

		# Connection frame
		connFrame = tk.Frame(self.root, bg='#262523')
		connFrame.place(relx=0.2, rely=0.2, relwidth=0.3, relheight=0.7, anchor='n')

		# Frame for Widget
		widgetFrame = tk.Frame(connFrame, bg='#464646')
		widgetFrame.place(relx=0.5, rely=0, relwidth=1.0, relheight=0.15, anchor='n')
		# IP Label
		self.ipLabel = tk.Label(widgetFrame, text="IP: XXX.XXX.X.X", bg='#464646', font='TkDefaultFont 10')
		self.ipLabel.place(relx=0, rely=0.15, relwidth=1.0, relheight=0.2)
		self.ipLabel.config(fg="#ababab")
		# IP Status
		self.ipStatus = tk.Label(widgetFrame, text="Status: Not Connected", bg='#464646', font='TkDefaultFont 10')
		self.ipStatus.place(relx=0, rely=0.55, relwidth=1.0, relheight=0.2)
		self.ipStatus.config(fg="#cd5c5c")

		if self.connected:
			self.ipLabel['text'] = 'IP: ' + TCP_IP
			self.ipStatus['text'] = 'Status: Connected'
			self.ipStatus.config(fg="#32cd32")

		# ----------------- #

		# Data frame
		dataFrame = tk.Frame(self.root, bg='#ababab')
		dataFrame.place(relx=0.67, rely=0.2, relwidth=0.525, relheight=0.7, anchor='n')

		# Threshold Title
		thresholdTitle = tk.Label(dataFrame, text="Thresholds:", bg='#ababab', font='TkDefaultFont 14 bold')
		thresholdTitle.place(relx=0, rely=0, relwidth=0.5, relheight=0.1)
		# Voltage Threshold Label and Entry
		voltageEntryThreshold = tk.Label(dataFrame, text="Voltage: ", bg='#ababab')
		voltageEntryThreshold.place(relx=0, rely=0.1, relwidth=0.25, relheight=0.1)
		voltageEntry = tk.Entry(dataFrame, font=40)
		voltageEntry.place(relx=0.25, rely=0.1, relwidth=0.25, relheight=0.1)
		# Current Threshold Label and Entry
		currentEntryThreshold = tk.Label(dataFrame, text="Current: ", bg='#ababab')
		currentEntryThreshold.place(relx=0, rely=0.2, relwidth=0.25, relheight=0.1)
		currentEntry = tk.Entry(dataFrame, font=40)
		currentEntry.place(relx=0.25, rely=0.2, relwidth=0.25, relheight=0.1)
		# Entry button submission
		thresholdEntryButton = tk.Button(dataFrame, text="OK", font=40, command=lambda: self.thresholdInputting(voltageEntry.get(), currentEntry.get()))
		thresholdEntryButton.place(relx=0.5, rely=0.15, relwidth=0.2, relheight=0.1)

		# OFF/ON Button
		self.togglePowerButton = tk.Button(dataFrame, text="OFF", font=40, command=lambda: self.powerInputting())
		self.togglePowerButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.1)

		# SYNC Button
		self.syncButton = tk.Button(self.root, text="SYNC", font=40, command=lambda: self.inputting('sync'))
		self.syncButton.place(relx=0.05, rely=0.9, relwidth=0.1, relheight=0.05)

		# Labels
		self.label = tk.Label(dataFrame, bg='#ababab')
		self.label.place(relx=0, rely=0.3, relwidth=1, relheight=0.8)

		self.connectedLabel = tk.Label(dataFrame, bg='#ababab')
		self.connectedLabel.place(relx=0, rely=0.3, relwidth=1, relheight=0.2)

		# Main loop
		self.root.mainloop()

	def run(self):
		t1 = threading.Thread(target=self.receiver, args=())
		t2 = threading.Thread(target=self.commands, args=())
		t1.start()
		t2.start()
		self.monitor()
		t1.join()
		t2.join()

if __name__ == "__main__":
	a = Application()
	a.run()