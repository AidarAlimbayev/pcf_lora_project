#!/usr/bin/sudo python3
import main_pcf_lib3 as pcf
import serial
from datetime import datetime, date, time
import csv
import logging

time.sleep(10)

logging.basicConfig(filename = 'pcf_file.log', level = logging.DEBUG, format='%(asctime)s %(message)s')
#logging.basicConfig(format='%(asctime)s %(message)s')
#logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s - line %(lineno)d") 

type_scales = "Scale_A" # Тип весов. Дано на каждые весы по отдельности
cow_id = "b'0700010101001e4b'" # Значение пустого ответа от считывателя
null_id = "b'0700010101001e4b'"
weight_finall = 0

logging.info('main: Start script')


# Часть кода для первого подключения к Ардуино
try:
    s = serial.Serial('/dev/ttyACM0',9600)
    print("main: connect arduino")
    logging.info('main: connect arduino')
    logging.info(s)
except Exception as e:
    print("main: Ошибка подключения к Ардуино, нету файла /dev/ttyACM0")
    logging.info('main: Arduino didnt connected')
    logging.info(e)
    print(e)
else:
    logging.info('main: else step Arduino')


def main():
    print ("main: Start script")
    logging.info('main: Start main code')

    while(True):
        logging.info('main: Infinite cycle')
        cow_id = pcf.Connect_RFID_reader()
        print("Cow ID: ")
        print(cow_id)
        
        if cow_id != '070106156079':
            
            logging.info('main: After read cow ID')
            logging.info(cow_id)
            
            weight_finall = pcf.Connect_ARD_get_weight(cow_id, s)
            logging.info('main: Weight: ')
            logging.info(weight_finall)
            
            if str(weight_finall) != '0':
                logging.info('main: Collect data to CSV')
                print('main: Collect data to CSV')
                pcf.Collect_data_CSV(cow_id, weight_finall, type_scales)
                logging.info('main: Send data to server')
                print('main: Send data to server')
                pcf.Send_data_to_server(cow_id, weight_finall, type_scales)
                cow_id = '070106156079'

main()