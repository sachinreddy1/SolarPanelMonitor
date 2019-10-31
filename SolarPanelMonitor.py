import threading
import curses
import socket
import json
import sqlite3
import time
import queue
import tkinter as tk

TCP_IP = '192.168.1.2'
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
					return					
				elif self.command == 'select':
					cursor.execute("SELECT * FROM voltages")
					ret = cursor.fetchall()
					self.label['text'] = self.formatSelect(ret)
					self.conn.commit()
				elif self.command == 'delete':
					cursor.execute("DELETE FROM voltages")
					self.conn.commit()
				self.command = None

	# ----------------- #

	def receiver(self):
		
		while True:
			try:
				self.s.connect((TCP_IP, TCP_PORT))
				self.s.send(MESSAGE)	
				self.lastData = self.s.recv(BUFFER_SIZE)
			except:
				pass

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
		root = tk.Tk()
		
		root.winfo_toplevel().title("Solar Panel Monitor")
		root.geometry('{}x{}'.format(WIDTH, HEIGHT))
		root.configure(bg='#383735')

		frame = tk.Frame(root, bg='#80c1ff', bd=5)
		frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
		entry = tk.Entry(frame, font=40)
		entry.place(relwidth=0.65, relheight=1)
		button = tk.Button(frame, text="Get", font=40, command=lambda: self.inputting(entry.get()))
		button.place(relx=0.7, relheight=1, relwidth=0.3)
		lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
		lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')
		self.label = tk.Label(lower_frame)
		self.label.place(relwidth=1, relheight=1)
		root.mainloop()

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