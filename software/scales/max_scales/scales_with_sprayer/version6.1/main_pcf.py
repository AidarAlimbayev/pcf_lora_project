#!/usr/bin/python3 

"""Scales main file without sprayer. Version 6.1
by Alimbayev Aidar and Suieubayev Maxat."""

import _headers as hdr

requirement_list = ['loguru', 'requests', 'pyserial']
hdr.install_packages(requirement_list)

import lib_pcf as pcf
import time
#time.sleep(10)
from datetime import datetime, time
from loguru import logger
import _config as cfg
import time


logger.add('log/scales_{time}.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")             # Настройка логгера

@logger.catch()         # Показывает ошибки, не работает если их обрабатывать
def main():
    try:
        type_scales = cfg.get_setting("Parameters", "serial_number") # Забираем серийный номер из config.ini
        port = cfg.get_setting("Parameters", "arduino_port")    # Забираем порт
        pcf.calibrate_or_start()    # Выбор между калибровкой и измерением. 
        while True:
            cow_id = pcf.connect_rfid_reader()  # Считывание меток
            if cow_id != '435400040001':  
                arduino = pcf.start_obj(port)   # Создаем объект
                time.sleep(1)   # задержка для установления связи между rasp и arduino
                
                weight_finall, weight_array, weighing_start_time = pcf.measure_weight(arduino, cow_id) 
                    # Основное измерение
                
                logger.info("main: weight_finall", weight_finall) 
                weighing_end_time = str(datetime.now()) # Время окончания измерения

                if str(weight_finall) > '0':
                    logger.info("main: Send data to server")
                    pcf.post_array_data(type_scales, cow_id, weight_array, weighing_start_time, weighing_end_time)
                    pcf.post_median_data(cow_id, weight_finall, type_scales) # Send data to server by JSON post request
                arduino.disconnect() # Закрываем связь
    except Exception as k:
        arduino.disconnect()
        logger.error(f'Main error: {k}')
                

main()