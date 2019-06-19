#!/usr/bin/env python
   
import socket
    
    
TCP_IP = '192.168.0.250'
TCP_PORT = 27001
BUFFER_SIZE = 1024
#MESSAGE = "04ff211995"
   
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(bytearray([0x04, 0xff, 0x50, 0x17, 0xf7]))

data = s.recv(BUFFER_SIZE)
s.close()


print repr(data)
# print data.decode("utf-16")


for ch in data:
    code = ord(ch)
    print code