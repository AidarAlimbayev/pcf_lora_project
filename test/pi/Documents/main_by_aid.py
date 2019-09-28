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
# variables used
type_scales = 'typeA' #type of scales
weignt=''
date_now=''

###########################################
# TCP connection settings and socket
TCP_IP = '192.168.0.250'
TCP_PORT = 27001
BUFFER_SIZE = 1024


def Collect_data_CSV():
        ##############################################
        # collect all data into csv file
        i = i + 1
        print (i, animal_id, date_now, mid_weight, type_scales)
        
        
        row = [i, animal_id, date_now, mid_weight, type_scales]
        with open('cows.csv', 'a', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerow(row)
        writeFile.close()
        mid_weight = 0;


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

def Connect_ARD_get_weight():
    ############################################
    # Connection to arduino and collection data of weight
    s = serial.Serial('/dev/ttyACM0',9600)
    print("VALUE:")
    Centner=100
    weight = str(s.readline())
    weight=re.sub("b|'|\r|\n", "", weight[:-5])
    #print(re.sub("b|'|\r|\n", "", weight[:-5]))
    print(weight)
    i_of_weight = 1
    weight_buff = 0
    ###########################################
    # Collecting and averaging data of weight
    weight_list = []
    mid_weight = 0
    while float(weight) < 100:
        i_of_weight += 1
        weight = str(s.readline())
        weight = float(re.sub("b|'|\r|\n", "", weight[:-5]))
        weight_list.append(weight)
        print('Value of weight:', weight)
        #weight_buff = weight + weight_buff
    else:
        if len(weight_list)==0:
            print("NuLL WEIGHT EXCEPTION")
        else:
            del weight_list[len(weight_list)-1]
            #weight_list.remove(len(weight_list)-1)
            for y in weight_list:
                    mid_weight = mid_weight + y
            mid_weight = mid_weight / len(weight_list)
            print(mid_weight)
            animal_id = "b'0700010101001e4b'"

        



################################################
# TCP Socket connection
def Connect_RFID_reader():
        animal_id = "b'0700010101001e4b'"
        null_id = "b'0700010101001e4b'"
        
        while animal_id == null_id:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(bytearray([0x06, 0x00, 0x01, 0x04, 0xff, 0xd4, 0x39])) #
            data = s.recv(BUFFER_SIZE)
            animal_id= str(binascii.hexlify(data))
            s.close()
            #null_id = "b'0700010101001e4b'"
            #print("check", null_id)
        
        if animal_id == null_id:
            print("ID null")
            return (0)
        else:
            print("ID checkt")
            print("Animal ID", animal_id)
            
            
            Connect_ARD_get_weight() 
            return (1)


        


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
#iter = 0
#while iter < 100:
    #iter += 1
while 1:
    Connect_RFID_reader()
        #()        
        
        #bus.write_byte(SLAVE_ADDRESS,ord(j))
    #Send_data_to_server()
    #Collect_data_CSV()
    #time.sleep(10)
#iter = 0