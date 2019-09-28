####################################################
# libraries for this code
from datetime import datetime, date, time
import serial
import time
import socket
import json
import requests
import binascii
import csv

#####################################################
# variables used
type_scales = 'typeA' #type of scales
a=[]
val=0
datatext=''
weignt=''
date_now=''

###########################################
# TCP connection settings and socket
TCP_IP = '192.168.0.250'
TCP_PORT = 27001
BUFFER_SIZE = 1024

################################################
# TCP Socket connection

def Connect_RFID_reader():
        #animal_id = 0
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(bytearray([0x06, 0x00, 0x01, 0x04, 0xff, 0xd4, 0x39])) #
        data = s.recv(BUFFER_SIZE)
        animal_id= str(binascii.hexlify(data))
        print("Animal ID", animal_id)
        s.close()
        null_id = "b'0700010101001e4b'"
        #print("check", null_id)
        if animal_id == null_id:
            print("ID null")
            return (0)
        else:
            print("ID checkt")
            return (1)
        #animal_id = 0
while 1:
    Connect_RFID_reader()