#!/usr/bin/python3
import datetime
import json

import requests
import socket
import binascii
import statistics
import re
from loguru import logger 
import RPi.GPIO as GPIO 
from collections import Counter
import _hx711 as HX
import _config as cfg
import time
import threading
import queue
import sys


def connect_rfid_reader():                                      # Connection to RFID Reader through TCP and getting cow ID in str format
    try:    
        logger.debug(f'START RFID FUNCTION')
        TCP_IP = '192.168.1.250'                                #chafon 5300 reader address
        TCP_PORT = 60000                                        #chafon 5300 port
        BUFFER_SIZE = 1024
        animal_id = "b'435400040001'"                           # Id null starting variable
        animal_id_new = "b'435400040001'"
        null_id = "b'435400040001'"
        logger.debug(f'START Animal ID animal_id: {animal_id}')
        logger.debug(f'START Null id null_id : {null_id}')
    
        if animal_id == null_id: # Send command to reader waiting id of animal
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(bytearray([0x53, 0x57, 0x00, 0x06, 0xff, 0x01, 0x00, 0x00, 0x00, 0x50])) #Chafon RU5300 Answer mode reading mode command
            data = s.recv(BUFFER_SIZE)
            animal_id= str(binascii.hexlify(data))
            animal_id_new = animal_id[:-5] #Cutting the string from unnecessary information after 4 signs 
            animal_id_new = animal_id_new[-12:] #Cutting the string from unnecessary information before 24 signs
            logger.debug(f'Raw ID animal_id: {animal_id}')
            logger.debug(f'New ID animal_id_new: {animal_id_new}')
            logger.debug(f'Null id null_id : {str(null_id)}')
            s.close()             
        if animal_id_new == null_id: # Id null return(0)
            connect_rfid_reader()
        else: # Id checkt return(1)
            animal_id = "b'435400040001'"
            logger.debug(f'Success step 2 RFID. animal id new: {animal_id_new}')
            return(animal_id_new)
    except Exception as e:
        logger.error(f'Error connect to RFID {e}')
    else: 
        logger.debug(f'2 step RFID')


def post_median_data(animal_id, weight_finall, type_scales): # Sending data into Igor's server through JSON
    try:
        logger.debug(f'START SEND DATA TO SERVER:')
        url = 'http://194.4.56.86:8501/api/weights'
        headers = {'Content-type': 'application/json'}
        data = {"AnimalNumber" : animal_id,
                "Date" : str(datetime.datetime.now()),
                "Weight" : weight_finall,
                "ScalesModel" : type_scales}
        answer = requests.post(url, data=json.dumps(data), headers=headers, timeout=3)
        logger.debug(f'Answer from server: {answer}') # Is it possible to stop on this line in the debug?
        logger.debug(f'Content from main server: {answer.content}')
    except Exception as e:
        logger.error(f'Error send data to server {e}')
    else:
        logger.error(f'4 step send data')


def post_array_data(type_scales, animal_id, weight_list, weighing_start_time, weighing_end_time):
    try:
        logger.debug(f'Post data function start')
        url = 'https://smart-farm.kz:8502/v2/OneTimeWeighings'
        headers =  {'Content-Type': 'application/json; charset=utf-8'}
        data = {
                "ScalesSerialNumber": type_scales,
                "WeighingStart": weighing_start_time,
                "WeighingEnd": weighing_end_time,
                "RFIDNumber": animal_id,
                "Data": weight_list
                }  
        post = requests.post(url, data=json.dumps(data), headers=headers, timeout=3)
        logger.debug(f'Answer from server: {post}') # Is it possible to stop on this line in the debug?
        logger.debug(f'Content from main server: {post.content}')
    except Exception as e:
        logger.error(f'Error post data: {e}')


def measure_weight(hx):
    try:
        weight_arr = []
        weight = hx.calc_mean()
        start_timedate = str(datetime.datetime.now())    
        next_time = time.time()+1
        while weight > 10:
            weight = hx.calc_mean()
            current_time = time.time()
            time_to_wait = next_time - current_time
            if time_to_wait < 0:
                weight_arr.append(Counter(hx.get_arr()).most_common(1)[0][0])
                next_time = time.time()+1
                logger.debug(f'Common filter weights: {weight_arr}')

        if not weight_arr:
            logger.error("Error, null weight list")
            return 0, [], ''
        
        weight_finall = statistics.median(weight_arr)
        logger.debug(f'{type(weight_finall)}, {type(weight_arr)}, {type(start_timedate)}')
        return weight_finall, weight_arr, start_timedate

    except Exception as e:
        logger.error(f'measure_weight Error: {e}')


def connect_ard_get_weight(s): # Connection to aruino through USB by Serial Port
    try:
        s.flushInput() 
        s.flushOutput()
        weight = (str(s.readline())) # Start of collecting weight data from Arduino
        weight_new = re.sub("b|'|\r|\n", "", weight[:-5]) # 35.55 
        weight_list = []
        start_timedate = str(datetime.datetime.now())        

        while (float(weight_new) > 10): # Collecting weight to array 
            weight = (str(s.readline())) # wait something from arduino 
            weight_new = re.sub("b|'|\r|\n", "", weight[:-5]) # convert data from ard
            weight_list.append(float(weight_new))
            logger.debug(f'{weight_list}')

        if not weight_list:
            logger.error("Error, null weight list")
            return 0, [], ''

        else:
            if len(weight_list) > 1: # Here must added check on weight array null value and one element array
                del weight_list[-1]
            weight_finall = statistics.median(weight_list)
            logger.debug(f'{type(weight_finall)}, {type(weight_list)}, {type(start_timedate)}')
            return weight_finall, weight_list, start_timedate

    except Exception as e:
        logger.error(f"Error connection to Arduino {e}")
    except TypeError as t:
        logger.error(f'Cannot unpack non-iterable NoneType object {t}')


def calibrate():
    try:
        logger.info('Start calibrate function')

        GPIO.setmode(GPIO.BCM)  
        hx = HX.HX711(26,19)
        input("Remove any items from scale. Press any key when ready.")
        offset = hx.calib_read()
        logger.info("Value at zero (offset): {}".format(offset))
        hx.set_offset(offset)

        logger.info("Please place an item of known weight on the scale.")
        input("Press any key to continue when ready.")
        measured_weight = (hx.calib_read()-hx.get_offset())
        item_weight = input("Please enter the item's weight in kg.\n>")
        scale = int(measured_weight)/int(item_weight)
        hx.set_scale(scale)
        logger.info(f"Scale adjusted for kilograms: {scale}")
        logger.info(f'Offset: {offset}, set_scale(scale): {scale}')

        GPIO.cleanup()
        cfg.update_setting("Calibration", "Offset", offset)
        cfg.update_setting("Calibration", "Scale", scale)
        return offset, scale
    except:
        logger.error(f'calibrate Fail')
        cleanAndExit()


def __get_input(message, channel): # Функция для получения введенного значения
                                   # Ничего не менять!
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


def cleanAndExit():
    logger.info("Cleaning up...")
    GPIO.cleanup()
    logger.info("Bye!")
    sys.exit()
        
