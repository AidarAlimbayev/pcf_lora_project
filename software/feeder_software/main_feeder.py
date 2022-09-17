"""Feeder version 1. Edition by Suieubayev Maxat.
Contact number +7 775 818 48 43. Email maxat.suieubayev@gmail.com"""
#!/usr/bin/sudo python
import headers as hdr

requirement_list = ['loguru', 'requests', 'numpy', 'RPi.GPIO', 'pyserial', 'hx711']
hdr.install_packages(requirement_list)

import lib_feeder as fdr
from loguru import logger
import timeit
import requests
import serial
import json
from time import sleep
from requests.exceptions import HTTPError
import RPi.GPIO as GPIO
from hx711 import HX711
import sys, select

GPIO.setmode(GPIO.BCM)                 # set GPIO pin mode to BCM numbering
hx = HX711(dout_pin=21, pd_sck_pin=20)

i, o, e = select.select( [sys.stdin], [], [], 2 )
if (i): ratio = fdr.hx711_calibrate(hx)

logger.add('feeder.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")  

sleep(1)

feeder_type = "feeder_model_1"
type = "Feeder"
serial_number = "65545180001"
animal_id = "b'435400040001'"       #???????????????????
null_id = "b'435400040001'"         #???????????????????
weight_finall = 0                   #???????????????????
url = "https://smart-farm.kz:8502/api/v2/RawFeedings"
headers = {'Content-type': 'application/json'}


#try:
#    s = serial.Serial('/dev/ttyACM0',9600) 
#    logger.info(f'Connect arduino {s.name}')
#    logger.info(f'Configuration of serial: {s}')
#except Exception as e:
#    logger.error(f'Error to connection to arduino, there is no file: /dev/ttyACM0 {e}')
#else:
#    logger.error(f'Success: Arduino connected')

def main():
    while True:
        dist = fdr.distance()
        print("dist")
        print(dist)
        #distance = fdr.measuring_start(dist)
        #logger.info("measuring dist", distance)
        #print(distance)
        if dist<=10:
            start_weight = fdr.raspberry_weight()
            print("Start weight")
            print(start_weight)
            start_time = timeit.default_timer
            print("Start time")
            print(start_time)
            animal_id = fdr.rfid_label()
            print("RFID label")
            print(animal_id)
            logger.info(f'First step cow ID :{animal_id}')

            #sleep(1)
            
            if animal_id != '435400040001':  #?????????????????????
                logger.info(f'After read cow ID :{animal_id}')
                while dist <= 10:
                    print("While True")
                    sleep(1)
                    dist = fdr.distance()
                    print("dist")
                    print(dist)
                end_time = timeit.default_timer
                end_weight = fdr.raspberry_weight()
                print("end weight")
                print(end_weight)
                feed_time = int(start_time) - int(end_time)
                print("feed_time")
                print(feed_time)
                final_weight = int(start_weight) - int(end_weight)
                print("final_weight")
                print(final_weight)
                post_data = fdr.post_request(feeder_type, serial_number, feed_time, animal_id, final_weight, end_weight)
                try:
                    post = requests.post(url, data = json.dumps(post_data), headers = headers, timeout=0.5)
                    print(post)
                    #post.raise_for_status()
                except HTTPError as http_err:
                    logger.error(f'HTTP error occurred: {http_err}')
                except Exception as err:
                    logger.error(f'Other error occurred: {err}')

main()
