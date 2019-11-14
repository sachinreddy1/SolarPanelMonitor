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

	def scan(self, i):
		address = IP + str(i) 
		res = subprocess.call(['ping', '-q', '-c', '1', address]) 

		if res == 0: 
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket.setdefaulttimeout(1)
			s.settimeout(1)
	        try:
		        s.connect((address, TCP_PORT))
		        s.send("Something.")
		        print "---> CONNECTED | " + address + " <---"
		       	self.connections.append(Connection(s, address, TCP_PORT, True))  
	    	except Exception, e:
	        	pass
        	
	# def connect(self):
	# 	for i in range(1,NUM_CONNECTIONS): 
	# 		self.threads.append(threading.Thread(target=self.scan, args=(i,)))
			
	# 	for t in self.threads:
	# 		t.start()

	# 	for t in self.threads:
	# 		t.join()

	def connect(self):
  		for i in range(1,NUM_CONNECTIONS): 
 			self.scan(i)
		print len(self.connections)

	def clear(self):
		for i in self.connections:
			i.socket.close()

		self.connections = []
		self.threads = []

if __name__ == "__main__":
	c = Connector()
	c.connect()

	print len(c.connections)
	for i in c.connections:
		print i.ip
		print i.connected
		i.socket.close()

