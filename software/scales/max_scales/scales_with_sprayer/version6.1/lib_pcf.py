#!/usr/bin/python3

"""File containing all working functions and algorithms for determining the weight of the animal and spraying.
Author: Aidar Alimbayev and Suieubayev Maxat
Contact: maxat.suieubayev@gmail.com
Number: +7 775 818 48 43"""

from datetime import datetime
import json
import requests
import queue
import socket
import binascii
import timeit
import full_spray as fs
import statistics
import _config as cfg
import threading
import time
from loguru import logger
import values_class as value_data
import adc_data as ADC
import RPi.GPIO as GPIO

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


def start_filter(obj):
    try:
        for i in range(5):
            obj.calc_mean()
            obj.set_arr([])
    except Exception as e:
        logger.error(f'start filter function Error: {e}')


def connect_rfid_reader():  # Connection to RFID Reader through TCP and getting cow ID in str format
    try:
        logger.debug(f'START RFID FUNCTION')
        TCP_IP = '192.168.1.250'  # chafon 5300 reader address
        TCP_PORT = 60000  # chafon 5300 port
        BUFFER_SIZE = 1024
        animal_id = "b'435400040001'"  # Id null starting variable
        animal_id_new = "b'435400040001'"
        null_id = "b'435400040001'"
        logger.debug(f'START Animal ID animal_id: {animal_id}')
        logger.debug(f'START Null id null_id : {null_id}')

        if animal_id == null_id:  # Send command to reader waiting id of animal
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(bytearray([0x53, 0x57, 0x00, 0x06, 0xff, 0x01, 0x00, 0x00, 0x00,
                              0x50]))  # Chafon RU5300 Answer mode reading mode command
            data = s.recv(BUFFER_SIZE)
            animal_id = str(binascii.hexlify(data))
            animal_id_new = animal_id[:-5]  # Cutting the string from unnecessary information after 4 signs
            animal_id_new = animal_id_new[-12:]  # Cutting the string from unnecessary information before 24 signs
            logger.debug(f'Raw ID animal_id: {animal_id}')
            logger.debug(f'New ID animal_id_new: {animal_id_new}')
            logger.debug(f'Null id null_id : {str(null_id)}')
            s.close()
        if animal_id_new == null_id:  # Id null return(0)
            connect_rfid_reader()
        else:  # Id check return(1)
            animal_id = "b'435400040001'"
            logger.debug(f'Success step 2 RFID. animal id new: {animal_id_new}')
            return animal_id_new
    except Exception as e:
        logger.error(f'Error connect to Arduino {e}')
    else:
        logger.debug(f'2 step RFID')


def post_median_data(animal_id, weight_finall, type_scales): # Sending data into Igor's server through JSON
    try:
        logger.debug(f'START SEND DATA TO SERVER:')
        url = cfg.get_setting("Parameters", "median_url")
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
        url = cfg.get_setting("Parameters", "array_url")
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
    except Exception as e:
        logger.error(f'calibrate Fail: {e}')
        arduino.disconnect()

def measure_weight(obj, cow_id):
    try:
        weight_arr = []
        start_filter(obj)
        start_timedate = str(datetime.now())
        next_time = time.time()+1       
        type_scales = cfg.get_setting("Parameters", "serial_number")
        drink_start_time, gpio_state, weight_list, start_timedate = timeit.default_timer(), False, [], str(datetime.now()) # Sprayer
        values = value_data.Values(drink_start_time, 0, type_scales, cow_id, 0, '0', 0, 0, 0, 0, True)  # Sprayer
        weight_on_moment = obj.get_measure()
        while weight_on_moment > 10:
            obj.calc_mean()          
            current_time = time.time()
            time_to_wait = next_time - current_time
            if values.flag == False:
                gpio_state = fs.spray_main_function(gpio_state, values) # Sprayer
                values = fs.new_start_timer(gpio_state, values)     # Sprayer
            else:
                if time_to_wait < 0:
                    if round(time.time(), 0) % 5 == 0:
                        values.flag = False              # Sprayer
            if time_to_wait < 0:
                weight_arr.append(obj.calc_mean())
                next_time = time.time()+1
                logger.debug(f'Array weights: {weight_arr}')
            weight_on_moment = obj.get_measure()            

        GPIO.cleanup()
        if not weight_arr:
            logger.error("Error, null weight list")
            return 0, [], ''
        
        weight_finall = statistics.median(weight_arr)
        gpio_state = fs.gpio_state_check(gpio_state, values) # Spryaer
        #logger.debug(f'{type(weight_finall)}, {type(weight_arr)}, {type(start_timedate)}')
        return weight_finall, weight_arr, start_timedate

    except Exception as e:
        logger.error(f'measure_weight Error: {e}')
        GPIO.cleanup()
