#!/usr/bin/python3
import datetime
import json
import serial

from requests.exceptions import HTTPError

import requests
import socket
import binascii
import statistics
import re
from loguru import logger 


try:
    s = serial.Serial('/dev/ttyAMA0',9600)                      # path inside rapberry pi to arduino into dev folder
    logger.debug(f'Connect arduino {s.name}')
    logger.debug(f'Configuration of serial: {s}')
except Exception as e:
    logger.error(f'Error to connection to arduino, there is no file: /dev/ttyACM0 {e}')
    logger.error(f'If arduino installed right check "/dev/tty*". AMA, ACM, USB - Arudino\n.')
    logger.error(f'Rename s = serial.Serial("/dev/ttyACM0",9600) in main_pcf.py\n.')


def connect_ard_get_weight(s): # Connection to aruino through USB by Serial Port
    try:
        s.flushInput() 
        s.flushOutput()
        weight = (str(s.readline())) # Start of collecting weight data from Arduino
        weight_new = re.sub("b|'|\r|\n", "", weight[:-5]) # 35.55 
        start_timedate = str(datetime.datetime.now())        
        return start_timedate, weight_new

    except Exception as e:
        logger.error(f"Error connection to Arduino {e}")
    except TypeError as t:
        logger.error(f'Cannot unpack non-iterable NoneType object {t}')

def main_test():
    print(f'Start main test arduino...')
    while(1):
        time, weight =  connect_ard_get_weight(s)
        print(f'{time} weight is: {weight}\n')
        
main_test()
