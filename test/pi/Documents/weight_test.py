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
    while float(weight) > 100:
        i_of_weight += 1
        weight = str(s.readline())
        weight = float(re.sub("b|'|\r|\n", "", weight[:-5]))
        weight_list.append(weight)
        print('Value of weight:', weight)
        #weight_buff = weight + weight_buff
    else :
        null = 0.0
        del weight_list[len(weight_list)-1]
        #weight_list.remove(len(weight_list)-1)
        for y in weight_list:
                mid_weight = mid_weight + y
        mid_weight = mid_weight / len(weight_list)
        print(mid_weight)
        
Connect_ARD_get_weight()
        
