"""config.py - это модуль для создания, получения и обновления значении в конфиг файле.

После создания файла congif.ini будет выглядить примерно так:
 [Parameters]
 feeder_type = feeder_model_1
 type = Feeder
 serial_number = 65545180001
 median_url = http://194.4.56.86:8501/api/weights
 array_url = https://smart-farm.kz:8502/v2/OneTimeWeighings
 arduino_port = dev/ttyUSB0

 [Calibration]             - вот это section
 offset = 0                - а вот это setting
 scale = 0                 - а вот это setting

 [DbId]
 id = 0
 version = 6.1

 Важно помнить, вся информация в конфиг файле хранится в str
 Edition by Suieubayev Maxat.
 Contact number +7 775 818 48 43. Email maxat.suieubayev@gmail.com"""

#!/usr/bin/python3

import configparser
import os
from loguru import logger

path = "config.ini"         # Название конфиг файла config.ini

def create_config():        # Функция создания конфиг файла
    try:
        config = configparser.ConfigParser()
        config.add_section("Parameters")
        config.add_section("Calibration")         
        config.add_section("DbId")          
        config.set("Parameters", "model", "feeder_model_1")    
        config.set("Parameters", "type", "Feeder") 
        config.set("Parameters", "serial_number", "65545180001") 
        config.set("Parameters", "url", "https://smart-farm.kz:8502/api/v2/RawFeedings") 
        config.set("Parameters", "median_url", "http://194.4.56.86:8501/api/weights") 
        config.set("Parameters", "array_url", "https://smart-farm.kz:8502/v2/OneTimeWeighings") 
        config.set("Parameters", "arduino_port", "dev/ttyUSB0") 
        config.set("Calibration", "Offset", "8456818.125")    
        config.set("Calibration", "Scale", "5784.8" )
        config.set("DbId", "id", "0" ) 
        config.set("DbId", "version", "6.1" )        
        with open(path, "w") as config_file:
            config.write(config_file)
    except ValueError as e:
        logger.error(f'Config.py, create_config func error {e}')

 
def get_config(path):           # Получить доступ к конфиг файлу 
    try:
        if not os.path.exists(path):
            create_config(path)
        
        config = configparser.ConfigParser()
        config.read(path)
        return config
    except ValueError as e:
        logger.error(f'Config.py, get_config func error {e}')
 

def get_setting(section, setting):      # Поучить значение определенной переменной
    try:
        config = get_config(path)
        value = config.get(section, setting)
        return value
    except ValueError as e:
        logger.error(f'Config.py, get_setting func error {e}')
 
 
def update_setting(section, setting, value):    # Обновить значение
    try: 
        config = get_config(path)
        config.set(section, setting, str(value))
        with open(path, "w") as config_file:
            config.write(config_file)
    except ValueError as e:
        logger.error(f'Config.py, update_setting func error {e}')
 
