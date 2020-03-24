#####################################################
# 
from datetime import datetime, date, time
import serial
import smbus
import time
import socket
import json
import requests
import binascii

###########################################
# TCP connection settings and socket
TCP_IP = '192.168.0.250'
TCP_PORT = 27001
BUFFER_SIZE = 1024
a=[]
val=0
datatext=''
weight=''
dateN=''
def Connect():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(bytearray([0x06, 0x00, 0x01, 0x04, 0xff, 0xd4, 0x39]))
        data = s.recv(BUFFER_SIZE)
        datatext= str(binascii.hexlify(data));
        print "Animal ID", datatext)
        print 
        s.close()

##############################################
# I2C protocol connection with arduino
bus = smbus.SMBus(1)
SLAVE_ADDRESS = 0x04

###########################################
# sending data to Igor's server KazATU
while 1:
        dateN = str(datetime.now())
        print "Current Date"
        print dateN
        #print "ID Animal "
        #print datatext
        
        ############################################
        # Connection to arduino and collection data of weight        
        s = serial.Serial('/dev/ttyACM0',9600)
        print "VALUE:"
        weight = str(s.readline())
    
        i_of_weight = 0;
        weight_buff = 0;
        ###########################################
        # Collecting and averaging data of weight
        while weight > 100:
                i_of_weight++
                weight = str(s.readline())
                weight_buff = weight + weight_buff
        else:
        weight_finall = weight_buff / i_of_weight; # averagind data of weight by division by number of iterations
         i_of_weight = 0;
         weight_buff = 0;        

        print weight_finall
        if val!=0:
                Connect()
                time.sleep(0.5)
                for j in a:
 			bus.write_byte(SLAVE_ADDRESS,ord(j))
                print "Sending DATA TO SERVER:"
                url = 'http://87.247.28.238:8501/api/weights'
                headers = {'Content-type': 'application/json'}
                data = {"AnimalNumber" : datatext,
                        "Date" : "2019-07-1T19:51:00",
                        "Weight" : weight_finall,
                        "ScalesModel" : "test_1"}
                answer = requests.post(url, data=json.dumps(data), headers=headers)
                print("RESULT:",answer)
                response = answer.json()
                print(response)

                weight_finall = 0;

                time.sleep(10)
                a=[]
        else:
                val=1
                a=[]


