#!/usr/bin/python3
import datetime
import json
import requests
import socket
import binascii
import timeit
import statistics
import full_spray as fs
import re
from loguru import logger 

logger.add('scales.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip") #serialize="True")


def Send_RawData_to_server(animal_id, weight_new, type_scales, start_timedate): # Sending data into Igor's server through JSON
    try:
        url = 'http://194.4.56.86:8501/api/RawWeights'
        headers = {'Content-type': 'application/json'}
        data = {"AnimalNumber" : animal_id,
                "Date" : str(datetime.now()),
                "Weight" : weight_new,
                "ScalesModel" : type_scales,
                "RawWeightId" : start_timedate}
        answer = requests.post(url, data=json.dumps(data), headers=headers, timeout=1)
    except Exception as e:
        logger.error(f'Error send data to RawData server {e}')
    else:
        logger.error(f"4 step send RawData")
    
def Send_data_to_server(animal_id, weight_finall, type_scales): # Sending data into Igor's server through JSON
    try:
        url = 'http://194.4.56.86:8501/api/weights'
        headers = {'Content-type': 'application/json'}
        data = {"AnimalNumber" : animal_id,
                "Date" : str(datetime.now()),
                "Weight" : weight_finall,
                "ScalesModel" : type_scales}
        answer = requests.post(url, data=json.dumps(data), headers=headers, timeout=15)
        logger.info(f'{answer}')

    except Exception as e:
        logger.error(f'Error send data to server {e}')
    else:
        logger.error(f'4 step send data')

def Connect_RFID_reader():                                      # Connection to RFID Reader through TCP and getting cow ID in str format
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
            Connect_RFID_reader()
        else: # Id checkt return(1)
            animal_id = "b'435400040001'"
            logger.debug(f'Success step 2 RFID. animal id new: {animal_id_new}')
            return(animal_id_new)
    except Exception as e:
        logger.error(f'Error connect to Arduino {e}')
    else: 
        logger.debug(f'2 step RFID')
#########################################################################################################################

#########################################################################################################################
def Send_data_to_server(animal_id, weight_finall, type_scales): # Sending data into Igor's server through JSON
    try:
        logger.debug(f'START SEND DATA TO SERVER:')
        url = 'http://194.4.56.86:8501/api/weights'
        headers = {'Content-type': 'application/json'}
        data = {"AnimalNumber" : animal_id,
                "Date" : str(datetime.now()),
                "Weight" : weight_finall,
                "ScalesModel" : type_scales}
        answer = requests.post(url, data=json.dumps(data), headers=headers, timeout=3)
        logger.debug(f'Answer from server: {answer}') # Is it possible to stop on this line in the debug?
        logger.debug(f'Content from main server: {answer.content}')
    except Exception as e:
        logger.error(f'Error send data to server {e}')
    else:
        logger.error(f'4 step send data')
#########################################################################################################################

#########################################################################################################################
def Connect_ARD_get_weight(cow_id, s, type_scales): # Connection to aruino through USB by Serial Port
    try:
        weight_finall = 0
        drink_duration = 0
        s.flushInput() 
        s.flushOutput() 
        weight = (str(s.readline())) # Start of collecting weight data from Arduino

        weight_new = re.sub("b|'|\r|\n", "", weight[:-5])

        scales_list = {
                        'pcf_model_5': [40, 22],
                        'pcf_model_6': [40, 32],
                        'pcf_model_7': [40, 43],
                        'pcf_model_10': [40, 54]
                       }
        spray_get_url = 'https://smart-farm.kz:8502/api/v2/Sprayings?scalesSerialNumber='+type_scales+'&animalRfidNumber='+cow_id
        gpio_state = False
        weight_list = []
        start_timedate = str(datetime.now())
        drink_start_time = timeit.default_timer()


        while (float(weight_new) > 10): # Collecting weight to array
            weight = (str(s.readline()))
            weight_new = re.sub("b|'|\r|\n", "", weight[:-5])

            #################################################################################
            Send_RawData_to_server(cow_id, weight_new, type_scales, start_timedate)            
            gpio_state = fs.spray_main_function(drink_start_time, type_scales, scales_list, spray_get_url, cow_id, gpio_state)
            drink_start_time = fs.new_start_timer(drink_start_time, gpio_state)
            #################################################################################
            weight_list.append(float(weight_new))

        if weight_list == 0 or weight_list == []:
            logger.error("Error, null weight list")
        else:
            if weight_list != []: # Here must added check on weight array null value and one element array
                del weight_list[-1]
            
            weight_finall = statistics.median(weight_list)
            weight_list = []
            gpio_state = fs.gpio_state_check(scales_list, drink_start_time, spray_get_url, type_scales, cow_id, gpio_state)
            drink_end_time = timeit.default_timer()
            
            drink_duration = drink_end_time - drink_start_time

    except Exception as e:
        logger.error("Error connection to Arduino", e)
    else:
        weight_to_return = (float("{0:.2f}".format(weight_finall)))
        if weight_to_return != 0:
            return [weight_to_return, drink_duration]