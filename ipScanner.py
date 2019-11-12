import threading
import subprocess
import socket

from Connection import *

IP = "192.168.1."
ret = []
threads = []

def connect(ping):
    address = IP + str(ping) 
    res = subprocess.call(['ping', '-q', '-c', '1', address]) 

    if res == 0: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        try:
	        s.connect((address, 23))
	        s.send("Something.")
	       	ret.append(Connection(s, address, True))  
    	except Exception, e:
        	pass

for ping in range(1,5): 
	threads.append(threading.Thread(target=connect, args=(ping,)))

for t in threads:
	t.start()

for t in threads:
	t.join()

for i in ret:
	print i.ip
	print i.connected
	i.socket.close()