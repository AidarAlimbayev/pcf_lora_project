#!/usr/bin/env python
   
import socket
    
    
TCP_IP = '192.168.0.250'
TCP_PORT = 27001
BUFFER_SIZE = 1024
#MESSAGE = "04ff211995"
   
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(bytearray([0x04, 0xFF, 0x50, 0x17, 0xF7]))
data = s.recv(BUFFER_SIZE)
s.close()

# print ("received data: %x" %(str2hex(data)))
#print "received data:", data
print map(hex,bytearray(data))
#print ("received data: %x" str2hex(data))