#main_pcf_lib.py
from datetime import datetime, date, time
import serial
import time
import socket
import json
import requests
import binascii
import csv
import re

def Connect_ARD_get_weight():
        
        weight = (str(s.readline()))
        
        weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
        print(weight_new)

        weight_list = []
        mid_weight = 0
        while (float(weight_new) != 0): # Collecting weight to array 
            weight = (str(s.readline()))
            print("Weight :", weight)
            weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
            print("Substracted weight: ", weight_new)
            #float(weight_new)
            weight_list.append(float(weight_new))
        if weight_list == 0 or weight_list == []:
            return(0)
        else:
            if weight_list != 0:
                del weight_list[-1]
            weight_finall =  sum(weight_list) / len(weight_list) 
            weight_list = []
            return(float(weight_new))
    

def Connect_RFID_reader():
    ###########################################
    # TCP connection settings and socket
    TCP_IP = '192.168.0.250'
    TCP_PORT = 27001
    BUFFER_SIZE = 1024

    animal_id = "b'0700010101001e4b'" # Id null starting variable
    null_id = "b'0700010101001e4b'" # Id null

    print("Connect RFID state")
    
    if animal_id == null_id: # Send command to reader waiting id of animal
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(bytearray([0x06, 0x00, 0x01, 0x04, 0xff, 0xd4, 0x39])) #
        data = s.recv(BUFFER_SIZE)
        animal_id= str(binascii.hexlify(data))
        
        print("Received ID cow: ")
        print(animal_id)
        
        animal_id_new = animal_id[:-7]
        animal_id_new = animal_id_new[-24:]
        
        print("CUT ID cow: ")
        print(animal_id_new)
        
        
        s.close()             
    if animal_id_new == null_id: # Id null return(0)
        Connect_RFID_reader()
    else: # Id checkt return(1)
        
        return(animal_id_new)

    
def Send_data_to_server(animal_id, weight_finall, type_scales):
    print("Sending DATA TO SERVER:")
    url = ('http://87.247.28.238:8501/api/weights')
    headers = {'Content-type': 'application/json'}
    data = {"AnimalNumber" : animal_id,
            "Date" : str(datetime.now()),
            "Weight" : weight_finall,
            "ScalesModel" : type_scales}
    print(str(datetime.now))
    
    #answer = requests.post(url, data=json.dumps(data), headers=headers)
    try: 
        answer = requests.post(url, data=json.dumps(data), headers=headers)
    except expression as identifier:
        print(expression)
        
    #print("RESULT:",answer)
    #response = answer.json()
    #print(response)


def Collect_data_CSV(cow_id, weight_finall, type_scales):
    date_now = (str(datetime.now()))
    row = [cow_id, weight_finall,  date_now, type_scales]
    with open('cows_database.csv', 'a', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(row)
    writeFile.close()
    weight_finall = 0 

