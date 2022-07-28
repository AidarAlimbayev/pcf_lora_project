from datetime import datetime
import lib_pcf_spray as pcf
import requests
import timeit
import RPi.GPIO as GPIO
import time
import re


 
def distance():
    GPIO.setmode(GPIO.BCM)
    GPIO_TRIGGER = 18
    GPIO_ECHO = 24
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.output(GPIO_TRIGGER, True)                 # set Trigger to HIGH
    time.sleep(0.00001)                             # set Trigger after 0.01ms to LOW
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    while GPIO.input(GPIO_ECHO) == 0:               # save StartTime
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()                      # save time of arrival
    TimeElapsed = StopTime - StartTime              # time difference between start and arrival
    """multiply with the sonic speed (34300 cm/s)
     and divide by 2, because there and back"""
    distance = (TimeElapsed * 34300) / 2
    return distance
 
def measuring_start(distance):
    try:
        if distance <= 50:
            return True
        else:
            return False
    except ValueError as v:
        pcf.print_log(f'Measurement stopped {v}')

def post_request(feeder_type, serial_number, feed_time, animal_id, end_weight, feed_weight):
    try:
        payload = {
            "Eventdatetime": str(datetime.now()),
            "EquipmentType": feeder_type,
            "SerialNumber": serial_number,
            "FeedingTime": feed_time,
            "RFIDNumber": animal_id,
            "WeightLambda": end_weight,
            "FeedWeight": feed_weight
        }
        return payload
    except ValueError as v:
        pcf.print_log(f'Post_request function error: {v}')

def rfid_label():
    try:
        labels = []
        while len(labels) <= 11:
            cow_id = pcf.Connect_RFID_reader()
            labels.append(cow_id)
        animal_id = max([j for i,j in enumerate(labels) if j in labels[i+1:]]) if labels != list(set(labels)) else -1
        return animal_id
    except ValueError as v:
        pcf.print_log(f'Post_request function error: {v}')

def instant_weight(s):
    try:
        s.flushInput() 
        s.flushOutput() 
        weight = (str(s.readline())) 
        weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
        return weight_new
    except ValueError as e:
        pcf.print_log(f'Instant_weight function Error: {e}')


