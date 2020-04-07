#pcf_lib.py
from datetime import datetime, date, time
import time
import csv
import serial
import socket
import json
import requests
import binascii
import csv
import RPi.GPIO as GPIO #тут можно так сделать?

type_scales = "Scale_A"

#connect_id.py
def connect_id():
    print("Try to connect RFID")
    cow_id = str(input("Enter ID: "))
    if cow_id == 0:
        quit()
    else:
        return(float(cow_id))

#collect_data.py
def collect_data(cow_id, weight_finall):
    date_now = (str(datetime.now()))
    row = [cow_id, weight_finall,  date_now, type_scales]
    with open('test_algorithm.csv', 'a', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(row)
    writeFile.close()
    weight_finall = 0 

#connect_weight.py
def connect_weight():
    weight_list = []
    print("Measure weight of cow")
    weight = float(input("Enter weight: "))
    while (float(weight) != 0):
        weight = float(input("Enter weight:___"))
        weight_list.append(float(weight))
    if weight_list == 0 or weight_list == []:
        return(0)
    else:
        if weight_list != 0:
            print ("Weight list: ", weight_list)
            del weight_list[-1]

        weight_finall =  sum(weight_list) / len(weight_list) 
        weight_list = []
        return(float(weight_finall))

#send_server.py
def send_server(cow_id, weight_finall):
    print("ID:", cow_id)
    print("Weight:", weight_finall)
    print("Date:", str(datetime.now()))
    print ("Scale type:", type_scales)


def spray_func(spray_period)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT, GPIO.LOW)
    # подключение к базе
    # проверка данных да/нет
    #if spray_period/next_spray_time != 0
    # опрыскивание (GPIO вывод сигнала)
    GPIO.output(22, TRUE)
    #delay()
    #return()

def delay_wait()