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
import os
import timeit
import requests
import time
import json
import sys, select

"""Инициализация logger для хранения записи о всех действиях программы"""
logger.add('feeder.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")  

if not os.path.exists("config.ini"):    # Если конфиг файла не существует
    cfg.create_config("config.ini")     # Создать конфиг файл

sleep(1)


animal_id = "b'435400040001'"       
null_id = "b'435400040001'"        
#weight_finall = 0                  


@logger.catch
def main():
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
        logger.info(f'Start main')
        logger.info(f'Start measure')
        while True:
            try:        
                if time.time()%3600 == 0:
                    fdr.check_internet()
                ulrasonic_distance = fdr.distance() 
                logger.info(f'Distance: {ulrasonic_distance}') 

                if ulrasonic_distance < 60 or ulrasonic_distance > 120:  # переделать
                    logger.info(f'Let start begin')  
                    start_weight = fdr.measure()       # Nachalnii ves 150 kg
                    logger.info(f'Start weight: {start_weight}')    
                    start_time = timeit.default_timer()             # 15:30:40
                    logger.info(f'Start time: {start_time}')
                    animal_id = fdr.__connect_rfid_reader()                    # rfid 
                    logger.info(f'Animal_id: {animal_id}')
                    end_time = start_time      # 15:45:30
                    end_weight = start_weight
                    
                    if animal_id != '435400040001':
                        logger.info(f'Here is start while cycle')
                        while_flag = False
                        while (while_flag == False):
                            
                            end_time = timeit.default_timer()       
                            end_weight = fdr.measure() 
                            logger.info(f'Feed weight: {end_weight}')
                            logger.info(f'While is True')
                            time.sleep(1)
                            ulrasonic_distance = fdr.distance()
                            if ulrasonic_distance < 60 or ulrasonic_distance > 120:     # Переделать
                                while_flag = False
                            else:
                                while_flag = True
                            
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
            except (KeyboardInterrupt, SystemExit):
                fdr.cleanAndExit()


main()



