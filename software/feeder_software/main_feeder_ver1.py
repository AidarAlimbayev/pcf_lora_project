"""Feeder version 1. Edition by Suieubayev Maxat.
Contact number +7 775 818 48 43. Email maxat.suieubayev@gmail.com"""
#!/usr/bin/sudo python
import headers as hdr

requirement_list = ['loguru', 'requests', 'numpy', 'RPi.GPIO']
hdr.install_packages(requirement_list)

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

# GPIO.setmode(GPIO.BCM)                 # set GPIO pin mode to BCM numbering
# hx = HX711(d1ut_0in=21, pd_sck_pin=20)

i, o, e = select.select( [sys.stdin], [], [], 10)
if (i): 
    GPIO.setmode(GPIO.BCM)  
    hx = HX711(21, 20, gain=128)
    logger.info(f'Start calibration')
    offset, scale = fdr.calibrate() #Запись в файл



logger.add('feeder.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")  

sleep(1)


feeder_type = "feeder_model_1"
type = "Feeder"
serial_number = "65545180001"
animal_id = "b'435400040001'"       #???????????????????
null_id = "b'435400040001'"         #???????????????????
#weight_finall = 0                   #???????????????????
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


# @logger.catch
# def main():
#     logger.info(f'Start main')
#     while True:
#         ulrasonic_distance = fdr.distance()
#         logger.info(f'Distance: {ulrasonic_distance}')
#         #distance = fdr.measuring_start(ulrasonic_distance)
#         if ulrasonic_distance < 10:
#             logger.info(f'Start measure')
#             start_weight = fdr.raspberry_weight()
#             logger.info(f'Start weight: {start_weight}')
#             start_time = timeit.default_timer
#             logger.info(f'Start time: {start_time}')
#             animal_id = fdr.rfid_label()
#             logger.info(f'First step cow ID :{animal_id}')

#             sleep(1)
            
#             if animal_id != '435400040001':  #?????????????????????
#                 logger.info(f'After read cow ID :{animal_id}')
#                 while ulrasonic_distance < 10:
#                     end_time = timeit.default_timer
#                     end_weight = fdr.raspberry_weight()
#                     logger.info(f'End weight {end_weight}')
#                 feed_time = int(start_time) - int(end_time)
#                 final_weight = int(start_weight) - int(end_weight)
#                 logger.info(f'finall weight: {final_weight}')
#                 post_data = fdr.post_request(feeder_type, serial_number, feed_time, animal_id, final_weight, end_weight)
#                 try:
#                     post = requests.post(url, data = json.dumps(post_data), headers = headers, timeout=0.5)
#                     post.raise_for_status()
#                 except HTTPError as http_err:
#                     logger.error(f'HTTP error occurred: {http_err}')
#                 except Exception as err:
#                     logger.error(f'Other error occurred: {err}')


@logger.catch
def test_2():
    flag = False
    while not flag:
        GPIO.setmode(GPIO.BCM)  
        choice = input("[1] to calibrate\n"             #Выбор между калибровкой и началом измерении !!!!!!!!!!!
                        "[2] to start measure\n>")
        if choice == '1':
            offset, scale = fdr.calibrate()
        else:
            logger.info(f'Start main')
            logger.info(f'Start measure')
            while True:
                try:        
                    ulrasonic_distance = fdr.distance() #56.31, 33.44, 42.32, 9.11
                    logger.info(f'Distance: {ulrasonic_distance}') #print("Distance:", ultrasonic)
                    if ulrasonic_distance < 10:
                        logger.info(f'Let start begin')  
                        start_weight = fdr.measure(offset, scale)       # Nachalnii ves 150 kg
                        logger.info(f'Start weight: {start_weight}')    
                        start_time = timeit.default_timer()             # 15:30:40
                        logger.info(f'Start time: {start_time}')
                        animal_id = fdr.rfid_label()                    # rfid !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        logger.info(f'Animal_id: {animal_id}')
                        
                        if animal_id != '435400040001':
                            logger.info(f'Here is start while cycle')
                            while ulrasonic_distance < 10:
                                end_time = timeit.default_timer()       # 15:45:30
                                end_weight = fdr.measure(offset, scale) # 140 kg
                                logger.info(f'Your weight: {end_weight}')
                                logger.info(f'While is True')
                                ulrasonic_distance = fdr.distance()
                                time.sleep(1)
                            logger.info(f'While False.')
                            feed_time = end_time - start_time            #14:50
                            feed_time_rounded = round(feed_time, 2)
                            final_weight = start_weight - end_weight    #150-140=10
                            final_weight_rounded = round(final_weight, 2)
                            logger.info(f'Finall result')
                            logger.info(f'finall weight: {final_weight_rounded}')
                            logger.info(f'feed_time: {feed_time_rounded}')
                            post_data = fdr.post_request(feeder_type, serial_number, feed_time_rounded, animal_id, final_weight_rounded, end_weight)    #400
                            try:
                                post = requests.post(url, data = json.dumps(post_data), headers = headers, timeout=0.5)
                                post.raise_for_status()
                            except HTTPError as http_err:
                                logger.error(f'HTTP error occurred: {http_err}')
                            except Exception as err:
                                logger.error(f'Other error occurred: {err}')
                        
                except (KeyboardInterrupt, SystemExit):
                    flag = True
                    fdr.cleanAndExit()

            
@logger.catch
def test_loop():
    offset, scale = fdr.calibrate()
    i = 0
    while i < 1:
        try:
            hx = HX711(21, 20, gain=128)
            hx.set_scale(scale)
            hx.set_offset(offset)
            val = hx.get_grams()
            print(val)
            time.sleep(0.5)
        except:
            fdr.cleanAndExit()
test_2()
#test_loop()


