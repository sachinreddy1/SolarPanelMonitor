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

q = queue.LifoQueue()

class Application:
	def receiver(self):
		global q

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((TCP_IP, TCP_PORT))
		s.send(MESSAGE)

		conn = sqlite3.connect('solarPanel.db')
		cursor = conn.cursor()

		while True:
			data = s.recv(BUFFER_SIZE)
			try:
				packet = json.loads(data)
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

			if q.qsize() != 0:
				q.qsize()
				k = q.get()
				q.qsize()
				if k == 'q':
					print "Exiting."
					s.close()
					conn.close()
					return
				elif k == 'c':
					print "Creating database."
					cursor.execute("""CREATE TABLE voltages (
					timeRecorded integer,
					voltage_1 real,
					voltage_2 real,
					voltage_3 real,
					voltage_4 real
					)""")
					conn.commit()
				elif k == 's':
					print "Printing database."
					cursor.execute("SELECT * FROM voltages")
					ret = cursor.fetchall()
					for i in ret:
						print i
					conn.commit()
				elif k == 'd':
					print "Deleting database."
					cursor.execute("DELETE FROM voltages")
					conn.commit()

	def inputting(self):
	    global q
	    while True:
	    	# If not commands inputted
	        if q.qsize() == 0:
	        	# Request a command
	            k = raw_input("Enter a command: ")
	            # Store command in the queue
	            q.qsize()
                q.put(k)
                q.qsize()
                # If 'q', quit
            	if k == 'q':
	        		print "Inputting closed."
	        		return

	def run(self):
		t1 = threading.Thread(target=self.receiver, args=())
		t2 = threading.Thread(target=self.inputting, args=())
		t1.start()
		t2.start()
		t1.join()
		t2.join()

if __name__ == "__main__":
	a = Application()
	a.run()