#!/usr/bin/python3

"""The main file of the algorithm of weights with spraying.
Version 5.2.
Author: Alimbayev Aidar and Suieubayev Maxat
Contact: maxat.suieubayev@gmail.com
Number: +7 775 818 48 43"""

import headers as hdr

requirement_list = ['loguru', 'requests', 'RPi.GPIO', 'pyserial']
hdr.install_packages(requirement_list)

import lib_pcf as lib
import time
import serial
from datetime import datetime
from loguru import logger

time.sleep(10)
logger.add('scales.log', format="{time} {level} {message}",
           level="DEBUG", rotation="1 day", compression="zip")  # serialize="True")

type_scales = "pcf_model_5"
cow_id = "b'435400040001'"  # value of null answer of RFID reader
null_id = "b'435400040001'"
another_null_id = "b'435400040001'"
weight_final = 0

logger.info(f'main: Start script')

try:
    s = serial.Serial('/dev/ttyACM0', 9600)  # path inside raspberry pi to arduino into dev folder
    logger.debug(f'Connect arduino {s.name}')
    logger.debug(f'Configuration of serial: {s}')
except Exception as e:
    logger.error(f'Error to connection to arduino, there is no file: /dev/ttyACM0 {e}')
else:
    logger.error(f'Else step Arduino')


@logger.catch
def main():
    logger.debug(f'Start main script')

    while (True):
        cow_id = lib.connect_rfid_reader()
        if cow_id != '435400040001':  # Comparison to null cow_id answer
            logger.info("After read cow ID :", cow_id)
            """ Grab weight from arduino and collect to weight_final. """
            weight_final, weight_array, weighing_start_time = lib.connect_ard_get_weight(cow_id, s,
                                                                                         type_scales)
            logger.info("main: weight_final", weight_final)
            weighing_end_time = str(datetime.now())

            if str(weight_final) > '0':
                logger.info("main: Send data to server")
                lib.post_data(type_scales, cow_id, weight_array, weighing_start_time, weighing_end_time)
                lib.send_data_to_server(cow_id, weight_final, type_scales)  # Send data to server by JSON post request


main()
