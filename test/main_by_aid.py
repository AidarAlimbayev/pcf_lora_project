#####################################################
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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(bytearray([0x06, 0x00, 0x01, 0x04, 0xff, 0xd4, 0x39])) #
        data = s.recv(BUFFER_SIZE)
        animal_id= str(binascii.hexlify(data))
        print("Animal ID", animal_id)
        s.close()
        start_read_weight = 1
        retrun (start_read_weight)

def Connect_ARD_get_weight():
        ############################################
        # Connection to arduino and collection data of weight        
        s = serial.Serial('/dev/ttyACM0',9600)
        print("VALUE:")
        weight = str(s.readline())
    
        i_of_weight = 0
        weight_buff = 0
        ###########################################
        # Collecting and averaging data of weight
        while weight > 100:
                i_of_weight += 1
                weight = str(s.readline())
                weight_buff = weight + weight_buff
        else:
                weight_finall = weight_buff / i_of_weight # averagind data of weight by division by number of iterations
                i_of_weight = 0
                weight_buff = 0
                print(weight_finall)

def Collect_data_CSV():
        ##############################################
        # collect all data into csv file
        row = [i, animal_id, date_now, weight_finall, type_scales]
        with open('cows.csv', 'a', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(row)
        writeFile.close()
        weight_finall = 0;

def Send_data_to_server():
        ########################################
        # Sending data to Igor's server
        print("Sending DATA TO SERVER:")
        url = ('http://87.247.28.238:8501/api/weights')
        headers = {'Content-type': 'application/json'}
        data = {"AnimalNumber" : animal_id,
                "Date" : str(datetime.now()),
                "Weight" : weight_finall,
                "ScalesModel" : type_scales}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        print("RESULT:",answer)
        response = answer.json()
        print(response)

###############################################
# main program in infinite cycle
iter = 0
while iter < 100:
        iter += 1
              
        Connect_RFID_reader()
        if start_read_weight == 1
                Connect_ARD_get_weight()
        #bus.write_byte(SLAVE_ADDRESS,ord(j))
        Send_data_to_server()
        Collect_data_CSV()
        time.sleep(10)
        start_read_weight = 0
iter = 0