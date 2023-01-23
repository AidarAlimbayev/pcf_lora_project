"""Feeder version 3. Edition by Suieubayev Maxat.
feeder_module.py - это модуль функции кормушки. 
Contact number +7 775 818 48 43. Email maxat.suieubayev@gmail.com"""

#!/usr/bin/sudo python3

from requests.exceptions import HTTPError
from datetime import datetime
from loguru import logger
from hx7 import HX711
import sql_database as sql
import config as cfg
import RPi.GPIO as GPIO
import subprocess
import time
import requests
import binascii
import socket
import sys
import numpy
import json
import threading
import queue
import time
import re


# def distance():
#     try:
#         dist_list = []
#         while len(dist_list) < 10:
#             GPIO.setmode(GPIO.BCM)
#             GPIO_TRIGGER = 18
#             GPIO_ECHO = 24
#             GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
#             GPIO.setup(GPIO_ECHO, GPIO.IN)
#             GPIO.output(GPIO_TRIGGER, True)                 # set Trigger to HIGH
#             time.sleep(0.00001)                             # set Trigger after 0.01ms to LOW
#             GPIO.output(GPIO_TRIGGER, False)
#             StartTime = time.time()
#             StopTime = time.time()
#             while GPIO.input(GPIO_ECHO) == 0:               # save StartTime
#                 StartTime = time.time()
#             while GPIO.input(GPIO_ECHO) == 1:
#                 StopTime = time.time()                      # save time of arrival
#             TimeElapsed = StopTime - StartTime              # time difference between start and arrival
#             #"""multiply with the sonic speed (34300 cm/s)
#             #and divide by 2, because there and back"""
#             distance = (TimeElapsed * 34300) / 2
#             dist_list.append(distance)
#             GPIO.cleanup()
#         total = numpy.mean(dist_list)
        #total = max([j for i,j in enumerate(dist_list) if j in dist_list[i+1:]]) if dist_list != list(set(dist_list)) else -1
        #return round(total, 2)
    #except TypeError as t:
        #logger.error(f'Distance func error {t}')


def connect_arduino_to_get_dist(s):
    s.flushInput() # Cleaning buffer of Serial Port
    s.flushOutput() # Cleaning output buffer of Serial Port
    distance = (str(s.readline()))
    distance = re.sub("b|'|\r|\n", "", distance[:-5])
    while (float(distance)) < 50:
        distance = (str(s.readline()))
        distance = re.sub("b|'|\r|\n", "", distance[:-5])
        distance = float(distance)
        return distance
    return distance


def post_request(event_time, feed_time, animal_id, end_weight, feed_weight):
    try:
        feeder_type = cfg.get_setting("Parameters", "feeder_type")
        serial_number = cfg.get_setting("Parameters", "serial_number")
        payload = {
            "Eventdatetime": event_time,
            "EquipmentType": feeder_type,
            "SerialNumber": serial_number,
            "FeedingTime": feed_time,
            "RFIDNumber": animal_id,
            "WeightLambda": end_weight,
            "FeedWeight": feed_weight
        }
        return payload
    except ValueError as v:
        logger.error(f'Post_request function error: {v}')


def check_internet():
    try:
        mstr = "http://google.com"
        res = requests.get(mstr)
        if res.status_code == 200:
            sql.internetOn()
    except:
        logger.error(f'No internet')


def send_post(postData):
    post = 0
    url = cfg.get_setting("Parameters", "url")
    headers = {'Content-type': 'application/json'}
    try:
        post = requests.post(url, data = json.dumps(postData), headers = headers, timeout=5)
    except HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
    except Exception as err:
        logger.error(f'Other error occurred: {err}')
    finally:
        if type(post) != requests.models.Response:
            sql.noInternet(postData)


def __connect_rfid_reader():                                      # Connection to RFID Reader through TCP and getting cow ID in str format
    try:    
        logger.info(f'Start connect RFID function')
        TCP_IP = '192.168.1.250'                                #chafon 5300 reader address
        TCP_PORT = 60000                                        #chafon 5300 port
        BUFFER_SIZE = 1024
        animal_id = "b'435400040001'"                           # Id null starting variable
        animal_id_new = "b'435400040001'"
        null_id = "b'435400040001'"

        if animal_id == null_id: # Send command to reader waiting id of animal
            logger.info(f' In the begin: Animal ID: {animal_id}')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(bytearray([0x53, 0x57, 0x00, 0x06, 0xff, 0x01, 0x00, 0x00, 0x00, 0x50])) #Chafon RU5300 Answer mode reading mode command
            data = s.recv(BUFFER_SIZE)
            animal_id= str(binascii.hexlify(data))
            animal_id_new = animal_id[:-5] #Cutting the string from unnecessary information after 4 signs 
            animal_id_new = animal_id_new[-12:] #Cutting the string from unnecessary information before 24 signs
            logger.info(f'After end: Animal ID: {animal_id}')
            s.close()             
        if animal_id_new == null_id: # Id null return(0)
            __connect_rfid_reader()
        else: # Id checkt return(1)
            animal_id = "b'435400040001'"

            return animal_id_new
    except Exception as e:
        logger.error(f'Error connect RFID reader {e}')


def rfid_label():
    try:
        labels = []
        sec = 5
        start_time = time.time()
        stop_time = start_time + sec
        while len(labels) < sec:
            cow_id = __connect_rfid_reader()
            labels.append(cow_id)
            if time.time() >= stop_time:
                break

        if len(labels) < sec:
            animal_id = labels[-1]
        else:
            animal_id = max([j for i,j in enumerate(labels) if j in labels[i+1:]]) if labels != list(set(labels)) else -1
        return animal_id
    except ValueError as v:
        logger.error(f'Post_request function error: {v}')


def __get_input(message, channel): # Функция для получения введенного значения
                                   # Ничего не менять ее!
    response = input(message)
    channel.put(response)


def input_with_timeout(message, timeout):   # Функция создания второго потока.
                                            # Временная задержка во время которой можно ввести значение
                                            # Ничего не менять!
    channel = queue.Queue()
    message = message + " [{} sec timeout] ".format(timeout)
    thread = threading.Thread(target=__get_input, args=(message, channel))
    thread.daemon = True
    thread.start()

    try:
        response = channel.get(True, timeout)
        return response
    except queue.Empty:
        pass
    return None


# def instant_weight(s):
#     try:
#         s.flushInput() 
#         weight = (str(s.readline())) 
#         weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
#         return weight_new
#     except ValueError as e:
#         logger.error(f'Instant_weight function Error: {e}')


def calibrate():
    try:
        GPIO.setmode(GPIO.BCM)  
        logger.info('Start calibrate function')
        hx = HX711(21, 20, gain=128)
        readyCheck = input("Remove any items from scale. Press any key when ready.")
        offset = hx.read_average()
        logger.info("Value at zero (offset): {}".format(offset))
        hx.set_offset(offset)
        logger.info("Please place an item of known weight on the scale.")
        readyCheck = input("Press any key to continue when ready.")
        measured_weight = (hx.read_average()-hx.get_offset())
        item_weight = input("Please enter the item's weight in kg.\n>")
        scale = int(measured_weight)/int(item_weight)
        hx.set_scale(scale)
        logger.info("Scale adjusted for kilograms: {}".format(scale))
        logger.info(f'Offset: {offset}, set_scale(scale): {scale}')
        print("calibrate: offset", offset)
        print("calibrate: scale", scale)
        GPIO.cleanup()
        cfg.update_setting("Calibration", "Offset", offset)
        cfg.update_setting("Calibration", "Scale", scale)
        return offset, scale
    except:
        logger.error(f'calibrate Fail')


def cleanAndExit():
    logger.info("Cleaning up...")
    GPIO.cleanup()
    logger.info("Bye!")
    sys.exit()


def measure():
    try:
        GPIO.setmode(GPIO.BCM)  
        hx = HX711(21, 20, gain=128)
        offset = float(cfg.get_setting("Calibration", "Offset"))
        scale = float(cfg.get_setting("Calibration", "Scale"))
        hx.set_scale(scale)
        hx.set_offset(offset)
        val = hx.get_grams()
        hx.power_down()
        time.sleep(.001)
        hx.power_up()
        GPIO.cleanup()
        return round(val,2)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


def __function_timer(timeout_time):
    try:
        logger.info(f'Function timer')
        start = time.time()
        stop_seconds = timeout_time
        while time.time() - start < stop_seconds:
            None
        return False
    except:
        logger.error(f'function_timer error.')
