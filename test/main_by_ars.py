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
import re

#####################################################
# global variables used
type_scales = 'typeA' #type of scales
a=[]
val=0
datatext=''
weignt=''
date_now=''
animal_id = "b'0700010101001e4b'" # void animal id


###########################################
# TCP connection settings and socket
TCP_IP = '192.168.0.250'
TCP_PORT = 27001
BUFFER_SIZE = 1024


def Collect_data_CSV():  # Collect all data into csv file
        row = [i, animal_id, date_now, mid_weight, type_scales]
        with open('cows.csv', 'a', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(row)
        writeFile.close()
        mid_weight = 0;      
 
def Send_data_to_server():# Sending data to Igor's server
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

def Connect_ARD_get_weight(): # Connection to arduino and collection data of weight
    s = serial.Serial('/dev/ttyACM0',9600)
    weight = str(s.readline())
    weight=re.sub("b|'|\r|\n", "", weight[:-5])
    weight_list = []
    mid_weight = 0
    while float(weight) != 0: # Collecting weight to array 
        weight = str(s.readline())
        weight = float(re.sub("b|'|\r|\n", "", weight[:-5]))
        weight_list.append(weight)
        print('Value of weight:', weight)
    else:
        if len(weight_list) == 0 and sum(weight_list) == 0: # Check array to null lenth and null sum
                print("NuLL WEIGHT EXCEPTION")
                Connect_ARD_get_weight() # Return to connect arduino and collecting weight
        else:
                del weight_list[len(weight_list)-1]
                for y in weight_list:
                        mid_weight = mid_weight + y # Averaging weight 
                        if mid_weight == 0:
                                Connect_ARD_get_weight() # Return to connect arduino and collecting weight
                        else: 
                                mid_weight = mid_weight / len(weight_list)  
                                print("Averaged weight: ", mid_weight)
                                animal_id = "b'0700010101001e4b'"
                                return(mid_weight) # Output averaged weight from function


def Connect_RFID_reader(): # TCP Socket connection output animal_id
        animal_id = "b'0700010101001e4b'" # Id null
        null_id = "b'0700010101001e4b'" # Id null
        
        while animal_id == null_id: # Send command to reader waiting id of animal
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(bytearray([0x06, 0x00, 0x01, 0x04, 0xff, 0xd4, 0x39])) #
            data = s.recv(BUFFER_SIZE)
            animal_id= str(binascii.hexlify(data))
            s.close()             
        if animal_id == null_id: # Id null return(0)
            #print("ID null")
            return (0)
        else: # Id checkt return(1)
            #print("ID checkt")
            #print("Animal ID", animal_id)
            Connect_ARD_get_weight()
            return (animal_id)


while 1:
        animal_id = Connect_RFID_reader()
        print(animal_id)
        print("#########") 