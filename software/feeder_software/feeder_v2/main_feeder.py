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
from time import sleep
import _config as cfg
import os
import timeit
import time
import serial

"""Инициализация logger для хранения записи о всех действиях программы"""
logger.add('feeder.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")  
if not os.path.exists("config.ini"):    # Если конфиг файла не существует
    cfg.create_config("config.ini")     # Создать конфиг файл
animal_id = "b'435400040001'"       
null_id = "b'435400040001'"        
#weight_finall = 0     
       

#@logger.catch
def main():
    fdr.calibrate_or_start()
    logger.debug(f"------------------Start while True cycle---------------------")
    while True:
        try:        
            port = cfg.get_setting("Parameters", "arduino_port")     
            relay_pin = cfg.get_setting("Relay", "sensor_pin")

            if fdr.get_relay_state(int(relay_pin)):  # переделать
                arduino = fdr.start_obj(port)
                start_weight = fdr.first_weight(arduino)       # Nachalnii ves 150 kg
                logger.info(f'Start weight: {start_weight}')    
                start_time = timeit.default_timer()             # 15:30:40 datetime.datetime.now()
                logger.info(f'Start time: {start_time}')
                animal_id = fdr.__connect_rfid_reader()                    # rfid 
                logger.info(f'Animal_id: {animal_id}')
                end_time = start_time      # 15:45:30
                end_weight = start_weight

                if animal_id != '435400040001':
                    logger.info(f'Here is start while cycle')
                    
                    while fdr.get_relay_state(int(relay_pin)):
                        end_time = timeit.default_timer()       
                        end_weight = arduino.get_measure()
                        logger.info(f'Feed weight: {end_weight}')
                        time.sleep(1)
                        if fdr.get_relay_state(int(relay_pin)) == False: # На всякий случай
                            break
                        
                    logger.info(f'While ended.')
                    feed_time = end_time - start_time           
                    feed_time_rounded = round(feed_time, 2)
                    final_weight = start_weight - end_weight    
                    final_weight_rounded = round(final_weight, 2)
                    logger.info(f'Finall result')
                    logger.info(f'finall weight: {final_weight_rounded}')
                    logger.info(f'feed_time: {feed_time_rounded}')
                    eventTime = str(str(datetime.now()))
                    if feed_time > 10: # Если корова стояла больше 10 секунд то отправляем данные
                        post_data = fdr.post_request(eventTime, feed_time_rounded, animal_id, final_weight_rounded, end_weight)    #400
                        fdr.send_post(post_data)
                arduino.disconnect()
        except Exception as e:
            logger.error(f'Error: {e}')
            arduino.disconnect()


main()



