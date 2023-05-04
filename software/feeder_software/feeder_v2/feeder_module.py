"""Feeder version 3. Edition by Suieubayev Maxat.
feeder_module.py - это модуль функции кормушки. 
Contact number +7 775 818 48 43. Email maxat.suieubayev@gmail.com"""

#!/usr/bin/sudo python3

from requests.exceptions import HTTPError
from datetime import datetime
from loguru import logger
import sql_database as sql
import _config as cfg
import statistics
import adc_data as ADC
import time
import requests
import binascii
import socket
import sys
import json
import threading
import queue
import time
import re


def start_obj(port):
    try:
        obj = ADC.ArduinoSerial(port)
        obj.connect()
        offset, scale = float(cfg.get_setting("Calibration", "offset")), float(cfg.get_setting("Calibration", "scale"))
        obj.set_offset(offset)
        obj.set_scale(scale)
        return obj
    except Exception as e:
        logger.error(f'Error connecting: {e}')

def connect_arduino_to_get_dist(s):
    s.flushInput() # Cleaning buffer of Serial Port
    s.flushOutput() # Cleaning output buffer of Serial Port
    distance = (str(s.readline()))
    distance = re.sub("b|'|\r|\n", "", distance[:-5])
    #while (float(distance)) < 50:
    #    distance = (str(s.readline()))
    #    distance = re.sub("b|'|\r|\n", "", distance[:-5])
    #    distance = float(distance)
    #    return distance
    return distance


def post_request(event_time, feed_time, animal_id, end_weight, feed_weight):
    try:
        feeder_type = cfg.get_setting("Parameters", "type")
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
    url = cfg.get_setting("Parameters", "url")
    headers = {'Content-type': 'application/json'}
    try:
        post = requests.post(url, data = json.dumps(postData), headers = headers, timeout=30)
        logger.info(f'{post.status_code}')
    except HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
    except Exception as err:
        logger.error(f'Other error occurred: {err}')
    # finally:
    #     if type(post) != requests.models.Response:
    #         sql.noInternet(postData)


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

def calibrate_or_start():
    try:
        logger.info(f'("[1] to calibrate\n" "[2] to start measure\n>")')
        choice = '2'
        choice = input_with_timeout("Choice:", 5)
        time.sleep(5)

        if choice == '1':
            offset, scale = calibrate()
            cfg.update_setting("Calibration", "Offset", offset)
            cfg.update_setting("Calibration", "Scale", scale)

    except Exception as e:
        logger.error(f'Calibrate or start Error: {e}')


def calibrate():
    try:
        logger.info('Start calibrate function')
        port = cfg.get_setting("Parameters", "arduino_port")
        arduino = ADC.ArduinoSerial(port, 9600, timeout=1)
        arduino.connect()
        logger.info(f"Remove any items from scale. Press any key when ready.")
        time.sleep(1)
        input()
        offset = arduino.calib_read()
        logger.info("Value at zero (offset): {}".format(offset))
        arduino.set_offset(offset)
        logger.info("Please place an item of known weight on the scale.")

        input()
        measured_weight = (arduino.calib_read()-arduino.get_offset())
        logger.info("Please enter the item's weight in kg.\n>")
        item_weight = input()
        scale = int(measured_weight)/int(item_weight)
        arduino.set_scale(scale)
        logger.info(f"Scale adjusted for kilograms: {scale}")
        logger.info(f'Offset: {offset}, set_scale(scale): {scale}')

        cfg.update_setting("Calibration", "Offset", offset)
        cfg.update_setting("Calibration", "Scale", scale)
        arduino.disconnect()
        del arduino
        return offset, scale
    except:
        logger.error(f'calibrate Fail')
        arduino.disconnect()


def measure_weight(obj):
    try:
        weight = obj.calc_mean()
        #logger.debug(f'{type(weight_finall)}, {type(weight_arr)}, {type(start_timedate)}')
        return weight
    except Exception as e:
        logger.error(f'measure_weight Error: {e}')


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
