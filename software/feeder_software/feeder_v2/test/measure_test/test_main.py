import feeder_module as fdr
from loguru import logger
import _config as cfg
import os
import time

"""Инициализация logger для хранения записи о всех действиях программы"""
logger.add('feeder.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")  
if not os.path.exists("config.ini"):    # Если конфиг файла не существует
    cfg.create_config("config.ini")     # Создать конфиг файл


def main():
    fdr.calibrate_or_start()
    port = cfg.get_setting("Parameters", "arduino_port")  
    while True:
        arduino_start = fdr.start_obj(port)
        weight = fdr.measure_weight(arduino_start)
        logger.info(f"Weight is: {weight}\n")
        arduino_start.disconnect()
    

main()