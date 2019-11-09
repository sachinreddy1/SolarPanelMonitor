import subprocess 
import socket

for ping in range(1,10): 
    address = "192.168.1." + str(ping) 
    res = subprocess.call(['ping', '-q', '-c', '1', address]) 
    if res == 0: 
        print( "ping to", address, "OK")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
	        s.connect((address, 23))
	        s.send("Something.")
	        print address
	        print "----------> Connection successful. <----------"
    	except Exception, e:
        	print 'Connection failed.'
        s.close() 

    elif res == 2: 
        print("no response from", address) 
    else: 
        print("ping to", address, "failed!")
