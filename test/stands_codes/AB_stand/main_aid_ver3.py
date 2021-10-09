#!/usr/bin/sudo python3
import main_pcf_lib3 as pcf # Подключение библиотек основных функций
import time  
time.sleep(60) # Задержка на 60 секунд для ожидания запуска последовательного порта
from datetime import datetime, date, time
import serial
import csv 
import logging # Библиотека логгирования



#logging.basicConfig(filename = 'pcf_file.log', level = logging.DEBUG, format='%(asctime)s %(message)s')
#logging.basicConfig(format='%(asctime)s %(message)s')
#logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s - line %(lineno)d") 

type_scales = "Scale_A" # Тип весов. Дано на каждые весы по отдельности
cow_id = "b'0700010101001e4b'" # Значение пустого ответа от считывателя для первого запуска
null_id = "b'0700010101001e4b'" # Значение пустого ответа от считывателя
weight_finall = 0 # Пустая переменная для итогового веса

logging.info('--------------------------------------------------------') 
logging.info('main: Start script') # Фунция логирования начала осноной программы

# Часть кода для первого подключения к Ардуино
try:
    s = serial.Serial('/dev/ttyACM0',9600) # Настройка последовательного порта
    print("main: connect arduino") # Функция отметки вывода состояния в терминал
    print(s.name)
    logging.info('main: connect arduino') # Функция отметки вывода состояния в лог файл 
    logging.info(s)
    logging.info(s.name)
except Exception as e:
    print("main: Ошибка подключения к Ардуино, нету файла /dev/ttyACM0")
    logging.info('main: Arduino didnt connected')
    logging.info(e)
    print(e)
else:
    logging.info('main: else step Arduino')


def main(): # Основная часть алгоритма
    print ("main: Start script")
    logging.info('main: Start main code')

    while(True): # Бесконечный цикл программы
        logging.info('main: Infinite cycle')
        cow_id = pcf.Connect_RFID_reader() # Функция для считывания ID коровы
        print("Cow ID: ")
        print(cow_id)
        
        if cow_id != '070106156079': # Проверка на пустое ID
            
            logging.info('main: After read cow ID')
            logging.info(cow_id)
            
            weight_finall = pcf.Connect_ARD_get_weight(cow_id, s) # Функция для сбора данных о весе
            logging.info('main: Weight: ')
            logging.info(weight_finall)
            
            if str(weight_finall) != '0': # Проверка на пустой вес
                logging.info('main: Collect data to CSV')
                print('main: Collect data to CSV')
                pcf.Collect_data_CSV(cow_id, weight_finall, type_scales) # Функция для записи данных в табличный файл
                logging.info('main: Send data to server')
                print('main: Send data to server')
                pcf.Send_data_to_server(cow_id, weight_finall, type_scales) # Функиця отправки данных на сервер
                cow_id = '070106156079'

main() # Запуск программы
