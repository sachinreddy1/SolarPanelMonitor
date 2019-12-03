import socket
import threading
# import netifaces as ni
from Connection import *

TCP_PORT = 23
INIT_CONNECTION = 0
NUM_CONNECTIONS = 100
TIMEOUT = 10

class Connector:
   def __init__ (self):
      self.threads = []
      self.connections = []
      self.ip = None

   def scan(self, i):
      address = self.ip + str(i) 
      s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      s.settimeout(TIMEOUT)
      try:
         s.connect((address, TCP_PORT))
         self.connections.append(Connection(s, address, TCP_PORT, True)) 
      except:
         pass

   # ------------- #

   def connect(self):
      self.threads = []
      self.connections = []
      self.ip = self.get_ip_address().rpartition('.')[0] + "."

      for i in range(INIT_CONNECTION, INIT_CONNECTION + NUM_CONNECTIONS): 
         self.threads.append(threading.Thread(target=self.scan, args=(i,)))
      for t in self.threads:
         t.start()
      for t in self.threads:
         t.join()
      print ("DONE.")

   # ------------- #

   def findConnection(self, ip):
      for idx, i in enumerate(self.connections):
         if i.ip == ip:
            return idx
      return -1

   def clear(self):
      for i in self.connections:
         i.socket.close()

      self.connections = []
      self.threads = []

   # ------------- #

   def get_ip_address(self):
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.connect(("8.8.8.8", 80))
      return s.getsockname()[0]

if __name__ == "__main__":
   c = Connector()
   c.connect()

   print (len(c.connections))
   for i in c.connections:
      print (i.ip)
      print (i.connected)
      i.socket.close()
