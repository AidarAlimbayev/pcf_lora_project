#!/usr/bin/sudo python3
import main_pcf_lib3 as pcf
import serial
from datetime import datetime, date, time
import csv
import logging

pin = 14
pcf.Gpio_Setup(pin)

logging.basicConfig(filename = 'pcf_logs/pcf_file-%s.log' % str(datetime.now()), level = logging.DEBUG, format='%(asctime)s %(message)s')
#logging.basicConfig(format='%(asctime)s %(message)s')
#logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s - line %(lineno)d") 

type_scales = "Scale_A" # Scale type. Given for each scale separately
cow_id = "b'0700010101001e4b'" # The value of an empty response from the reader
null_id = "b'0700010101001e4b'"
weight_finall = 0

logging.info('main: Start script')


# Part of the code for the first connection to Arduino
try:
    s = serial.Serial("/dev/ttyACM0",9600)
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
    logging.info('main: Start script')

    while(True):
        logging.info('main: Infinite cycle')

        cow_id = pcf.Connect_RFID_reader()
        print("Cow ID: %s" % cow_id)
        
        if cow_id != '070106156079':
            
            logging.info('main: Get weight from Arduino')
            
            weight_finall = pcf.Connect_ARD_get_weight(cow_id, s)
            logging.info('main: Weight: %s' % str(weight_finall))

            
            
            if str(weight_finall) != '0':
                logging.info('main: Spray liquid drug')
                pcf.Spray_Func()

                logging.info('main: Collect data to CSV')
                print('main: Collect data to CSV')

                pcf.Collect_data_CSV(cow_id, weight_finall, type_scales)
                
                logging.info('main: Send data to server')
                print('main: Send data to server')
                
                pcf.Send_data_to_server(cow_id, weight_finall, type_scales)
                cow_id = '070106156079'
                weight_finall = 0
                weight = 0

main()
