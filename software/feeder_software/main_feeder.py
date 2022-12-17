"""Feeder version 2. Edition by Suieubayev Maxat.
Contact number +7 775 818 48 43. Email maxat.suieubayev@gmail.com"""
#!/usr/bin/sudo python3
import headers as hdr

requirement_list = ['loguru', 'requests', 'numpy', 'RPi.GPIO']
hdr.install_packages(requirement_list)

from datetime import datetime
import os
import feeder_test as fdr
from loguru import logger
import timeit
import requests
import time
import serial
import json
from time import sleep
from requests.exceptions import HTTPError
import RPi.GPIO as GPIO
from hx7 import HX711
import sys, select

logger.add('feeder.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")  

path = "config.ini"
section = "Calibration"

if not os.path.exists(path):
    fdr.create_config(path)

sleep(1)
feeder_type = "feeder_model_1"
type = "Feeder"
serial_number = "65545180001"
animal_id = "b'435400040001'"       #???????????????????
null_id = "b'435400040001'"         #???????????????????
#weight_finall = 0                   #???????????????????
url = "https://smart-farm.kz:8502/api/v2/RawFeedings"
headers = {'Content-type': 'application/json'}

# offset = float(fdr.get_setting(path, section, "Offset")) # offset = 3.12
# scale = float(fdr.get_setting(path, section, "Scale")) # scale = 3.13


@logger.catch
def main():

    GPIO.setmode(GPIO.BCM)  
    logger.info(f'("[1] to calibrate\n" "[2] to start measure\n>")')
    choice = '2'
    choice = fdr.input_with_timeout("Choice:", 5)
    time.sleep(5)
    if choice == '1':
        offset, scale = fdr.calibrate()
        fdr.update_setting(path, section, "Offset", offset)
        fdr.update_setting(path, section, "Scale", scale)
    else:
        logger.info(f'Start main')
        logger.info(f'Start measure')
        while True:
            try:        
                offset = float(fdr.get_setting(path, section, "Offset"))
                scale = float(fdr.get_setting(path, section, "Scale"))
                ulrasonic_distance = fdr.distance() #56.31, 33.44, 42.32, 9.11
                logger.info(f'Distance: {ulrasonic_distance}') #print("Distance:", ultrasonic)

                if ulrasonic_distance < 60 or ulrasonic_distance > 120:
                    logger.info(f'Let start begin')  
                    start_weight = fdr.measure(offset, scale)       # Nachalnii ves 150 kg
                    logger.info(f'Start weight: {start_weight}')    
                    start_time = timeit.default_timer()             # 15:30:40
                    logger.info(f'Start time: {start_time}')
                    animal_id = fdr.__connect_rfid_reader()                    # rfid !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    logger.info(f'Animal_id: {animal_id}')
                    end_time = start_time      # 15:45:30
                    end_weight = start_weight
                    
                    if animal_id != '435400040001':
                        logger.info(f'Here is start while cycle')
                        while_flag = False
                        while (while_flag == False):
                            end_time = timeit.default_timer()       # 15:45:30
                            end_weight = fdr.measure(offset, scale) # 140 kg
                            logger.info(f'Feed weight: {end_weight}')
                            logger.info(f'While is True')
                            time.sleep(1)
                            ulrasonic_distance = fdr.distance()
                            while_flag = ulrasonic_distance < 60 or ulrasonic_distance > 120 
                            
                        logger.info(f'While ended.')
                        feed_time = end_time - start_time            #14:50
                        feed_time_rounded = round(feed_time, 2)
                        final_weight = start_weight - end_weight    #150-140=10
                        final_weight_rounded = round(final_weight, 2)
                        logger.info(f'Finall result')
                        logger.info(f'finall weight: {final_weight_rounded}')
                        logger.info(f'feed_time: {feed_time_rounded}')
                        eventTime = str(str(datetime.now()))
                        post_data = fdr.post_request(feeder_type, serial_number, feed_time_rounded, animal_id, final_weight_rounded, end_weight)    #400
                        try:
                            post = requests.post(url, data = json.dumps(post_data), headers = headers, timeout=5)
                            post.raise_for_status()   # RESPONSE[200]
                        except HTTPError as http_err:
                            logger.error(f'HTTP error occurred: {http_err}')
                            save post_data to file.txt 
                        except Exception as err:
                            logger.error(f'Other error occurred: {err}')

                        else:
                            if file.txt != Null:
                                while (i not None)
                                i = 1
                                while(response == 200):
                                    open file.txt as f:
                                        post_data = [f'Save {i}']
                                    post = requests.post(url, data = json.dumps(post_data), headers = headers, timeout=5)
                                    response = post.raise_for_status()
                                    if response == 200:
                                        open file.txt as f:
                                            delete.[f'Save {i}']
                                    i+=1
            except (KeyboardInterrupt, SystemExit):
                fdr.cleanAndExit()


main()



