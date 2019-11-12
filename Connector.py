import threading
import subprocess
import socket
from Connection import *

IP = "192.168.1."
TCP_PORT = 23

NUM_CONNECTIONS = 10

class Connector:
	def __init__ (self):
		self.threads = []
		self.connections = []

	def ping(self, i):
		address = IP + str(i) 
		res = subprocess.call(['ping', '-q', '-c', '1', address]) 

		if res == 0: 
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(5)
	        try:
		        sock.connect((address, TCP_PORT))
		        sock.send("Something.")
		       	self.connections.append(Connection(sock, address, True))  
	    	except Exception, e:
	        	pass

	def connect(self):
		for i in range(1,NUM_CONNECTIONS): 
			self.threads.append(threading.Thread(target=self.ping, args=(i,)))
			
		for t in self.threads:
			t.start()

		for t in self.threads:
			t.join()

	def clear(self):
		for i in self.connections:
			i.socket.close()

		self.connections = []
		self.threads = []

if __name__ == "__main__":
	c = Connector()
	c.connect()
	for i in c.connections:
		print i.ip
		print i.connected
		i.socket.close()