#!/usr/bin/sudo python3
import lib_pcf_ver4 as pcf
import time

time.sleep(10)
from datetime import datetime, date, time

import serial
import csv
import logging



logging.basicConfig(filename = 'pcf_file.log', level = logging.DEBUG, format='%(asctime)s %(message)s')
#logging.basicConfig(format='%(asctime)s %(message)s')
#logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(funcName)s - line %(lineno)d") 

type_scales = "Test_raspberry_ver4" # Types of weights
cow_id = "b'0700010101001e4b'" # value of null answer of RFID reader
null_id = "b'0700010101001e4b'"
another_null_id = "b'435400040001'"
weight_finall = 0

logging.info('main: Start script')


# Connection to arduino
try:
    s = serial.Serial('/dev/ttyUSB0',9600) # path inside rapberry pi to arduino into dev folder
    pcf.print_log("Connect arduino", s.name)
    pcf.print_log("Configuration of serial: ", s)
except Exception as e:
    pcf.print_log("Error to connection to arduino, there is no file: /dev/ttyACM0", e)
else:
    pcf.print_log("Else step Arduino")


def main():
    pcf.print_log("Start main script")

    while(True):
        pcf.print_log("Infinite cycle")
        cow_id = pcf.Connect_RFID_reader() # Connection to RFID reader 
        pcf.print_log("First step cow ID :", cow_id)
        
        if cow_id != '435400040001': # Comparision to null cow_id answer 
            # second ID is also null 
            pcf.print_log("After read cow ID :", cow_id)
                        
            weight_finall = pcf.Connect_ARD_get_weight(cow_id, s, type_scales) # Grab weight from arduino and collect to weight_finall
            pcf.print_log("main: weight_finall", weight_finall)
                        
            if str(weight_finall) != '0':

                pcf.print_log("main: Collect data")
                pcf.Collect_data_CSV(cow_id, weight_finall, type_scales) # Save weight data into CSV file

                pcf.print_log("main: Send data to server")
                pcf.Send_data_to_server(cow_id, weight_finall, type_scales) # Send data to server by JSON post request
                #cow_id = '070106156079'
                cow_id = '435400040001'

main()