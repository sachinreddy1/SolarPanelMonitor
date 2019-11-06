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

TCP_IP = '192.168.1.4'
TCP_PORT = 23
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

HEIGHT = 500
WIDTH = 600

class Application:
	def __init__ (self):
		self.command = None
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.lastData = None
		self.root = None
		self.connected = False

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
				self.command = None

	# ----------------- #

	def receiver(self):

		# Check for a connection
		self.s.settimeout(5)
		try:
			self.s.connect((TCP_IP, TCP_PORT))
			self.connected = True
		except:
			self.connected = False

		if self.connected:
			self.s.send(MESSAGE)
		
		# Run the receiver
		while True:
			if self.connected:
				self.lastData = self.s.recv(BUFFER_SIZE)

			if self.command == 'quit':
				return

	def inputting(self, command):
		self.command = command

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

		entry = tk.Entry(frame, font=40, bg='#ababab')
		entry.place(relwidth=0.65, relheight=0.5)

		button = tk.Button(frame, text="Command", font=40, command=lambda: self.inputting(entry.get()))
		button.place(relx=0.7, relwidth=0.3, relheight=0.5)

		# Connection frame
		connFrame = tk.Frame(self.root, bg='#262523')
		connFrame.place(relx=0.2, rely=0.25, relwidth=0.3, relheight=0.6, anchor='n')

		# Data frame
		dataFrame = tk.Frame(self.root, bg='#ababab')
		dataFrame.place(relx=0.67, rely=0.25, relwidth=0.525, relheight=0.6, anchor='n')

		voltageEntry = tk.Entry(dataFrame, font=40) #, bg='#ababab')
		voltageEntry.place(relx=0, rely=0, relwidth=1, relheight=0.1)
		currentEntry = tk.Entry(dataFrame, font=40) #, bg='#ababab')
		currentEntry.place(relx=0, rely=0.1, relwidth=1, relheight=0.1)

		# Labels
		self.label = tk.Label(dataFrame, bg='#ababab')
		self.label.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)

		self.connectedLabel = tk.Label(dataFrame, bg='#ababab')
		self.connectedLabel.place(relx=0, rely=0.2, relwidth=1, relheight=0.2)

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