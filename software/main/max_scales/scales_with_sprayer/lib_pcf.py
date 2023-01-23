#!/usr/bin/python3

"""File containing all working functions and algorithms for determining the weight of the animal and spraying.
Author: Aidar Alimbayev and Suieubayev Maxat
Contact: maxat.suieubayev@gmail.com
Number: +7 775 818 48 43"""

from datetime import datetime
import json
import requests
import socket
import binascii
import timeit
import full_spray as fs
import statistics
import re
from loguru import logger
import Values_class as value_data


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


def send_data_to_server(animal_id, weight_final, type_scales):  # Sending data into Igor's server through JSON
    try:
        logger.debug(f'START SEND DATA TO SERVER:')
        url = 'http://194.4.56.86:8501/api/weights'
        headers = {'Content-type': 'application/json'}
        data = {"AnimalNumber": animal_id,
                "Date": str(datetime.now()),
                "Weight": weight_final,
                "ScalesModel": type_scales}
        answer = requests.post(url, data=json.dumps(data), headers=headers, timeout=3)
        logger.debug(f'Answer from server: {answer}')  # Is it possible to stop on this line in the debug?
        logger.debug(f'Content from main server: {answer.content}')
    except Exception as e:
        logger.error(f'Error send data to server {e}')
    else:
        logger.error(f'4 step send data')



def post_data(type_scales, animal_id, weight_list, weighing_start_time, weighing_end_time):
    try:
        logger.debug(f'Post data function start')
        url = 'https://smart-farm.kz:8502/v2/OneTimeWeighings'
        headers = {'Contet-type': 'application/json'}
        data = {
            "ScalesSerialNumber": type_scales,
            "WeighingStart": weighing_start_time,
            "WeighingEnd": weighing_end_time,
            "RFIDNumber": animal_id,
            "Data": weight_list
        }
        post = requests.post(url, data=json.dumps(data), headers=headers, timeout=0.5)
        logger.debug(f'Answer from server: {post}')  # Is it possible to stop on this line in the debug?
        logger.debug(f'Content from main server: {post.content}')
    except Exception as e:
        logger.error(f'Error post data: {e}')


def __get_weight(s) -> float:  # Get edited weight value from arduino 
    try:
        logger.info(f'Get weight from arduino.')
        weight = (str(s.readline()))  # Start of collecting weight data from Arduino
        return re.sub("b|'|\r|\n", "", weight[:-5])
    except Exception as e:
        logger.error("Error connection to Arduino", e)



def connect_ard_get_weight(cow_id, s, type_scales):  # Connection to arduino through USB by Serial Port
    try:
        s.flushInput()
        s.flusOutput()
        # weight = (str(s.readline()))
        # weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
        weight_new = __get_weight(s)
        drink_start_time, gpio_state, weight_list, start_timedate = timeit.default_timer(), False, [], str(datetime.now())
        values = value_data.Values(drink_start_time, 0, type_scales, cow_id, 0, '0', 0, 0, 0, 0)

        while float(weight_new) > 10:  # Collecting weight to array
            weight_new = __get_weight(s)
            # weight = (str(s.readline()))
            # weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
            # Send_RawData_to_server(cow_id, weight_new, type_scales, start_timedate)
            gpio_state = fs.spray_main_function(gpio_state, values)
            values = fs.new_start_timer(gpio_state, values)
            weight_list.append(float(weight_new))
            logger.info(f'Weight list {weight_list}')

        if not weight_list:
            logger.error("Error, null weight list")
            return 0

        else:
            if len(weight_list) > 1:
                del weight_list[-1]
            weight_final = statistics.median(weight_list)
            gpio_state = fs.gpio_state_check(gpio_state, values)
            return weight_final, weight_list, start_timedate
    except TypeError as t:
        logger.error(f'Cannot unpack non-iterable NoneType object: {t}')
    except Exception as e:
        logger.error("Error connection to Arduino", e)
