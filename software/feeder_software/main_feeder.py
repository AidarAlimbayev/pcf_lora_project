"""Feeder version 3. Edition by Suieubayev Maxat.
main_feeder.py - это файл с основной логикой работы кормушки. 
Contact number +7 775 818 48 43. Email maxat.suieubayev@gmail.com"""

#!/usr/bin/sudo python3

import headers as hdr

requirement_list = ['loguru', 'requests', 'numpy', 'RPi.GPIO']
hdr.install_packages(requirement_list)

from datetime import datetime
import feeder_module as fdr
from loguru import logger
import RPi.GPIO as GPIO
from time import sleep
from hx7 import HX711
import config as cfg
import lib_pcf as pcf
import os
import timeit
import requests
import time
import json
import sys, select
import serial 

"""Инициализация logger для хранения записи о всех действиях программы"""
logger.add('feeder.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")  

if not os.path.exists("config.ini"):    # Если конфиг файла не существует
    cfg.create_config("config.ini")     # Создать конфиг файл

sleep(1)


animal_id = "b'435400040001'"       
null_id = "b'435400040001'"        
#weight_finall = 0                  

# Connection to arduino
try:
    s = serial.Serial('/dev/ttyACM0',9600) # path inside rapberry pi to arduino into dev folder
    logger.info(f'Connect arduino {s.name}')
    logger.info(f'Configuration of serial, {s}')
except Exception as e:
    logger.info(f'Error to connection to arduino, there is no file: /dev/ttyACM0 {e}')
else:
    logger.info(f'Success: Arduino connected')


@logger.catch
def main():

    print("------------Start main function------------------")
    GPIO.setmode(GPIO.BCM)  
    logger.info(f'("[1] to calibrate\n" "[2] to start measure\n>")')
    choice = '2'
    choice = fdr.input_with_timeout("Choice:", 5)
    time.sleep(5)
    i = 0


    if choice == '1':
        offset, scale = fdr.calibrate()
        cfg.update_setting("Calibration", "Offset", offset)
        cfg.update_setting("Calibration", "Scale", scale)
    else:
        print("---------------Start main after calibration---------------")
        logger.info(f'Start main')
        logger.info(f'Start measure')
        while True:
            print("------------------Start while True function---------------------")
            try:        
                if time.time()%3600 == 0:
                    fdr.check_internet()
                ulrasonic_distance = fdr.connect_arduino_to_get_dist(s) 
                logger.info(f'ultrasonic distance: {ulrasonic_distance}')
                ulrasonic_distance = float(ulrasonic_distance)
                logger.info(f'ultrasonic distance: {ulrasonic_distance}')
                logger.info(f'Distance: {ulrasonic_distance}') 

                if ulrasonic_distance > 10 or ulrasonic_distance < 40:  # переделать
                    logger.info(f'Let start begin')  
                    start_weight = fdr.measure()       # Nachalnii ves 150 kg
                    logger.info(f'Start weight: {start_weight}')    
                    start_time = timeit.default_timer()             # 15:30:40 datetime.datetime.now()
                    logger.info(f'Start time: {start_time}')
                    animal_id = fdr.__connect_rfid_reader()                    # rfid 
                    logger.info(f'Animal_id: {animal_id}')
                    end_time = start_time      # 15:45:30
                    end_weight = start_weight


                    print("start time", start_time)
                    print("end_time", end_time)
                    print("end_weight", end_weight)
                    logger.info(f'start time: {start_time}')
                    logger.info(f'end_time : {end_time}')
                    logger.info(f'end_weight: {end_weight}')


                    if animal_id != '435400040001':
                        logger.info(f'Here is start while cycle')
                        while_flag = True
                        while (while_flag == True):
                            
                            end_time = timeit.default_timer()       
                            end_weight = fdr.measure() 
                            logger.info(f'Feed weight: {end_weight}')
                            logger.info(f'While is True')
                            time.sleep(1)
                            ulrasonic_distance = fdr.connect_arduino_to_get_dist(s)
                            logger.info(f' Ultrasonic distance: {ulrasonic_distance}')
                            ulrasonic_distance = float(ulrasonic_distance)
                            while_flag = ulrasonic_distance < 10 or ulrasonic_distance > 50    # Переделать
                            logger.info(f'white flag: {while_flag}')
                            #if while_flag == False:
                            #    break
                            #if ulrasonic_distance < 10 or ulrasonic_distance > 50:
                            #    while_flag = True
                            #else:
                            #    while_flag = False
                            
                        logger.info(f'While ended.')
                        feed_time = end_time - start_time           
                        feed_time_rounded = round(feed_time, 2)
                        final_weight = start_weight - end_weight    
                        final_weight_rounded = round(final_weight, 2)
                        logger.info(f'Finall result')
                        logger.info(f'finall weight: {final_weight_rounded}')
                        logger.info(f'feed_time: {feed_time_rounded}')
                        eventTime = str(str(datetime.now()))
                        post_data = fdr.post_request(eventTime, feed_time_rounded, animal_id, final_weight_rounded, end_weight)    #400
                        fdr.send_post(post_data)
                        
                        # Clean up on variables 
                        eventTime = 0
                        feed_time_rounded = 0     
                        animal_id = '435400040001'
                        final_weight_rounded = 0
                        end_weight = 0

                        

            except (KeyboardInterrupt, SystemExit):
                fdr.cleanAndExit()


main()