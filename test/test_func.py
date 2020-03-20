from datetime import datetime, date, time
import serial
import time
import socket
import json
import requests
import binascii
import csv
import re

cow_id = "test"
type_scales = "Scale_A"
s = serial.Serial('/dev/ttyACM0',9600)

def Connect_ARD_get_weight():
        
        weight = (str(s.readline()))
        
        weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
        print(weight_new)

        weight_list = []      
        date_now = (str(datetime.now()))
        row = [cow_id, weight_list,  date_now, type_scales]
        with open('cows_test.csv', 'a', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(row)
        writeFile.close()
        weight_new = 0 
        Connect_ARD_get_weight()

Connect_ARD_get_weight()