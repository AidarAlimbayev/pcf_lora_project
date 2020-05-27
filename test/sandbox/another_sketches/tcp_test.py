#!/usr/bin/env python
   
import socket
import binascii
    
    
TCP_IP = '192.168.1.250'
TCP_PORT = 60000
BUFFER_SIZE = 1024
#MESSAGE = "04ff211995"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
#s.send(bytearray([0x53, 0x57, 0x00, 0x03, 0xff, 0xe0, 0x74])) # Active mode command
s.send(bytearray([0x53, 0x57, 0x00, 0x06, 0xff, 0x01, 0x00, 0x00, 0x00, 0x50]))

while 1:


    data = s.recv(BUFFER_SIZE)
    data= str(binascii.hexlify(data))
    print("Old data")
    print(data)
    data = data[:-5] #Cutting the string from unnecessary information after 7 signs 
    data = data[-12:] #Cutting the string from unnecessary information before 24 signs
    print("Cutted data")       
    print(len(data))
    print(data)

    
s.close()

#print repr(data)
# print data.decode("utf-16")
#f = open('text_1.txt', 'w')
#f.write(data)
#f.close()

# for ch in data:
#     code = ord(ch)
#     print code
