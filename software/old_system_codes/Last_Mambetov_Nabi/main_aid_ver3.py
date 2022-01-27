#!/usr/bin/sudo python3
import main_pcf_lib3 as pcf
import time

time.sleep(60)
from datetime import datetime, date, time

import serial
import csv
import logging



logging.basicConfig(filename = 'pcf_file.log', level = logging.DEBUG, format='%(asctime)s %(message)s')
#logging.basicConfig(format='%(asctime)s %(message)s')
#logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s - line %(lineno)d") 

type_scales = "Mambetov-2" # Types of weights
cow_id = "b'0700010101001e4b'" # value of null answer of RFID reader
null_id = "b'0700010101001e4b'"
weight_finall = 0

logging.info('main: Start script')


# Connection to arduino
try:
    s = serial.Serial('/dev/ttyACM0',9600) # path inside rapberry pi to arduino into dev folder
    print("main: connect arduino")
    print(s.name)
    logging.info('main: connect arduino')
    logging.info(s)
    logging.info(s.name)
except Exception as e:
    print("main: Error to connection to arduino, there is no file: /dev/ttyACM0")
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
        cow_id = pcf.Connect_RFID_reader() # Connection to RFID reader 
        print("Cow ID: ")
        print(cow_id)
        
        if cow_id != '070106156079': # Comparision to null cow_id answer 
            
            logging.info('main: After read cow ID')
            logging.info(cow_id)
            
            weight_finall = pcf.Connect_ARD_get_weight(cow_id, s) # Grab weight from arduino and collect to weight_finall
            logging.info('main: Weight: ')
            logging.info(weight_finall)
            
            if str(weight_finall) != '0':
                logging.info('main: Collect data to CSV')
                print('main: Collect data to CSV')
                pcf.Collect_data_CSV(cow_id, weight_finall, type_scales) # Save weight data into CSV file
                logging.info('main: Send data to server')
                print('main: Send data to server')
                pcf.Send_data_to_server(cow_id, weight_finall, type_scales) # Send data to server by JSON post request
                cow_id = '070106156079'

main()
