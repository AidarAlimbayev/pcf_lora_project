#!/usr/bin/python3 

"""Scales main file without sprayer. Version 6.1
by Alimbayev Aidar and Suieubayev Maxat."""

import _headers as hdr

requirement_list = ['loguru', 'requests', 'pyserial']
hdr.install_packages(requirement_list)

import lib_test as pcf
import time
#time.sleep(10)
from datetime import datetime, time
from loguru import logger
import _config as cfg
import time
import requests
import sys, select
import serial
import os
import timeit
import json


logger.add('log/scales_{time}.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")             # Настройка логгера

try:
    s = serial.Serial('/dev/ttyACM1',9600) # path inside rapberry pi to arduino into dev folder
    logger.info(f'Connect arduino {s.name}')
    logger.info(f'Configuration of serial, {s}')
except Exception as e:
    logger.info(f'Error to connection to arduino, there is no file: /dev/ttyACM0 {e}')
else:
    logger.info(f'Success: Arduino connected')
    
@logger.catch()         # Показывает ошибки, не работает если их обрабатывать
def main():
    try:
        type_scales = cfg.get_setting("Parameters", "serial_number") # Забираем серийный номер из config.ini
        logger.info(f'Type_scales: {type_scales}')
        port = cfg.get_setting("Parameters", "arduino_port")    # Забираем порт
        logger.info(f'Port: {port}')
        pcf.calibrate_or_start()    # Выбор между калибровкой и измерением. 
        while True:
            cow_id = '435400040001'
            #cow_id = pcf.connect_rfid_reader()  # Считывание меток
            #logger.info(f'Animal_ID: {cow_id}')
            sensor_distance=pcf.connect_arduino_to_get_dist(s)
            sensor_distance = float(sensor_distance)
            logger.info(f'Distance: {sensor_distance}')
            #if sensor_distance < 40:
            if cow_id == '435400040001':
                #sensor_distance=pcf.connect_arduino_to_get_dist(s)
                #sensor_distance = float(sensor_distance)
                #if sensor_distance < 40: 
                arduino = pcf.start_obj(port)   # Создаем объект
                time.sleep(1)   # задержка для установления связи между rasp и arduino
                weight_finall, weight_array, weighing_start_time = pcf.measure_weight(arduino) 
                    # Основное измерение
                start_time=timeit.default_timer()
                logger.info(f'Start time: {start_time}')
                logger.info(f'Start_time: {weighing_start_time}')
                start_weight = weight_finall
                logger.info(f'Start weight: {start_weight}')
                cow_id = pcf.connect_rfid_reader()
                logger.info(f'Animal_ID: {cow_id}')
                #logger.info("main: weight_finall", weight_finall)
                #cow_id = pcf.connect_rfid_reader()
                weighing_end_time = str(datetime.now()) # Время окончания измерения
                end_time = start_time
                end_weight = start_weight
                if sensor_distance < 40:
                    while_flag = True
                    while (while_flag == True):
                        end_time = timeit.default_timer()
                        logger.info(f'End_time: {end_time}')
                        weight_finall, weight_array, weighing_start_time = pcf.measure_weight(arduino) 
                        end_weight = weight_finall
                        logger.info(f'End_weight: {end_weight}')
                        time.sleep(1)
                        sensor_distance=pcf.connect_arduino_to_get_dist(s)
                        logger.info(f'Sensor_distance: {sensor_distance}')
                        try:
                            sensor_distance = float(sensor_distance)
                        except ValueError:
                            sensor_distance=pcf.connect_arduino_to_get_dist(s)
                        while_flag = int(sensor_distance) < 50
                        logger.info(f'White_flag: {while_flag}')
                    logger.info(f'While_ended')
                    feed_time = end_time - start_time
                    logger.info(f'Feed_time: {feed_time}')
                    feed_time_rounded = round(feed_time, 2)
                    logger.info(f'Feed_time_rounded: {feed_time_rounded}')
                    final_weight = start_weight - end_weight
                    logger.info(f'Final_weight: {final_weight}')
                    final_weight_rounded = round(final_weight, 2)
                    logger.info(f'Final_weight: {final_weight_rounded}')
                    #logger.info(f'Feed_time: {feed_time_rounded}')
                    eventTime = str(str(datetime.now()))
                    if str(final_weight) > '0':
                        logger.info("main: Send data to server")
                        pcf.post_array_data(type_scales, feed_time_rounded, cow_id, weight_array, final_weight_rounded)
                        pcf.post_median_data(eventTime, feed_time_rounded, cow_id, final_weight_rounded, start_time, end_time, end_weight) # Send data to server by JSON post request
                    arduino.disconnect() # Закрываем связь
                    eventTime = 0
                    logger.info(f'{eventTime}')
                    feed_time_rounded = 0  
                    logger.info(f'{feed_time_rounded}')   
                    cow_id = '435400040001'
                    logger.info(f'{cow_id}')
                    final_weight_rounded = 0
                    end_weight = 0
    except Exception as k:
        arduino.disconnect()
        logger.error(f'Main error: {k}')
                

main()
