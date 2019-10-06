from datetime import datetime, date, time
import time
import socket
import json
import requests
import binascii
import csv
import re

cow_id = ''
weight_list = [0]
weight = 0
weight_finall = 0
date_now = ''
type_scales = "Scale_A"
row = []

def connect_weight():
    print("Measure weight of cow")
    weight = float(input("Enter weight: "))
    while (float(weight) != 0):
        weight = input("Enter weight:_")
        weight_list.append(float(weight))
        #connect_weight()
    del weight_list[-1]
    if weight_list == 0:
        return(0)
    else:
        weight_finall =  sum(weight_list) / len(weight_list) 
        weight_list = []
        return(weight_finall)
    

def connect_id():
    print("Try to connect RFID")
    cow_id = str(input("Enter ID: "))
    return(cow_id)
    
def send_server():
    print("ID:", id)
    print("Weight:", weight_finall)
    print("Date:", str(datetime.now()))
    print ("Scale type:", type_scales)

def collect_data():
    date_now = (str(datetime.now()))
    #cow_id = '0'
    #weight_finall = 0
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
    cow_id = connect_id()
    if cow_id != 0:
        weight_finall = connect_weight()
        if weight_finall != 0:
            send_server()
            collect_data()
        else:
            #return(0)
            main()
    else:
        #return(0)
        main() 

main()