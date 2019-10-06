from datetime import datetime, date, time
import time
import socket
import json
import requests
import binascii
import csv
import re


weight = 0
weight_finall = 0
date_now = ''
type_scales = "Scale_A"
row = []
animal_id = "b'0700010101001e4b'"

def connect_weight():
    weight_list = []
    print("Measure weight of cow")
    weight = float(input("Enter weight: "))
    while (float(weight) != 0):
        weight = input("Enter weight:___")
        weight_list.append(float(weight))
        
        #connect_weight()
    
    if weight_list == 0 or weight_list == []:
        return(0)
    else:
        if weight_list != 0:
            print ("Weight list: ", weight_list)
            del weight_list[-1]

        weight_finall =  sum(weight_list) / len(weight_list) 
        weight_list = []
        return(weight_finall)
    

def connect_id():
    print("Try to connect RFID")
    cow_id = str(input("Enter ID: "))
    if cow_id == 0:
        connect_id()
    else:
        return(cow_id)
    
def send_server(animal_id, weight_finall):
    #print("ID:", cow_id)
    #print("Weight:", weight_finall)
    #print("Date:", str(datetime.now()))
    #print ("Scale type:", type_scales)

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


def collect_data(cow_id, weight_finall):
    date_now = (str(datetime.now()))
    row = [cow_id, weight_finall,  date_now, type_scales]
    with open('test_algorithm.csv', 'a', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(row)
    writeFile.close()
    weight_finall = 0; 


#weight_finall = connect_weight()
#print("Weight finall:", weight_finall)

#id = connect_id()
#print(id)

def main():
    cow_id = float(connect_id())
    if float(cow_id) != 0:
        weight_finall = float(connect_weight())
        if float(weight_finall) != 0:
            send_server(cow_id, weight_finall)
            collect_data(cow_id, weight_finall)
            main()
        else:
            #return(0)
            main()
    else:
        #return(0)
        main() 

main()