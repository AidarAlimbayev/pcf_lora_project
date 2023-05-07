#!/usr/bin/sudo python3
import feeder_module as fdr
from loguru import logger
import _config as cfg
import os
import serial
import time

"""Инициализация logger для хранения записи о всех действиях программы"""
logger.add('logs/feeder.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")  

if not os.path.exists("config.ini"):    # Если конфиг файла не существует
    cfg.create_config("config.ini")     # Создать конфиг файл


def main():
    dist_port = '/dev/ttyUSB_Dist'
    try:
        s = serial.Serial(dist_port,9600)
    except Exception as e:
        logger.error(f'Ошибка в {dist_port}: {e}')
    while True:
        time.sleep(0.1)
        ulrasonic_distance = fdr.connect_arduino_to_get_dist(s) 
        logger.info(f'ultrasonic distance sleep 0.1: {ulrasonic_distance}')
        logger.info(f'ultrasonic distance sleep 0.1 - type float: {float(ulrasonic_distance)}')
        time.sleep(1)
        ulrasonic_distance = fdr.connect_arduino_to_get_dist(s) 
        logger.info(f'ultrasonic distance sleep 1: {ulrasonic_distance}')
        logger.info(f'ultrasonic distance sleep 1 - type float: {float(ulrasonic_distance)}')
        time.sleep(2)
        ulrasonic_distance = fdr.connect_arduino_to_get_dist(s) 
        logger.info(f'ultrasonic distance sleep 2: {ulrasonic_distance}')
        logger.info(f'ultrasonic distance sleep 2 - type float: {float(ulrasonic_distance)}')
        time.sleep(4)
        ulrasonic_distance = fdr.connect_arduino_to_get_dist(s) 
        logger.info(f'ultrasonic distance sleep 4: {ulrasonic_distance}')
        logger.info(f'ultrasonic distance sleep 4 - type float: {float(ulrasonic_distance)}')


main()