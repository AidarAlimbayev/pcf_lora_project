#!/usr/bin/python3
import datetime
import json

from requests.exceptions import HTTPError

import requests
import socket
import binascii
import statistics
import re
from loguru import logger 


type_scales = "Scales_10_test"

logger.add('feeder.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")  

test_dict = {"animal_id": 'test0test101', 
                          "Date": str(datetime.datetime.now()), 
                          "Weight" : 100,
                          "weight_array":[100,150,50,100,50,150],
                          "weighing_start_time": str(datetime.datetime.now()),
                          "weighing_end_time":str(datetime.datetime.now()),
                          "ScalesModel" : type_scales}

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

#########################################################################################################################

#########################################################################################################################
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


def main_test():
    try:
        post_array_data(type_scales, test_dict["animal_id"], 
                    test_dict["weight_array"], 
                    test_dict["weighing_start_time"], 
                    test_dict["weighing_end_time"])
        post_median_data(test_dict["animal_id"], test_dict["Weight"], type_scales)

    except HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
    except Exception as err:
        logger.error(f'Other error occurred: {err}')

def main_test2():

        post_array_data(type_scales, test_dict["animal_id"], 
                    test_dict["weight_array"], 
                    test_dict["weighing_start_time"], 
                    test_dict["weighing_end_time"])
        post_median_data(test_dict["animal_id"], test_dict["Weight"], type_scales)


main_test2()