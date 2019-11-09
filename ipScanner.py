import subprocess 
import socket

IP = "192.168.1."

ret = []

for ping in range(1,5): 
    address = IP + str(ping) 
    res = subprocess.call(['ping', '-q', '-c', '1', address]) 

    if res == 0: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
	        s.connect((address, 23))
	        s.send("Something.")
	        ret.append(address)
    	except Exception, e:
        	pass
        s.close() 

print ret