#!/usr/bin/sudo python
import pcf_lib_test as pcf
import time

time.sleep(10)
from datetime import datetime, date, time
from loguru import logger
import serial


logger.add('scales.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")             #serialize="True")

type_scales = "pcf_model_5" 
cow_id = "b'435400040001'"                                      # value of null answer of RFID reader
null_id = "b'435400040001'"
another_null_id = "b'435400040001'"
weight_finall = 0

#logger.info(f'main: Start script')

try:
    s = serial.Serial('/dev/ttyUSB0',9600)                      # path inside rapberry pi to arduino into dev folder
    logger.debug(f'Connect arduino {s.name}')
    logger.debug(f'Configuration of serial: {s}')
except Exception as e:
    logger.error(f'Error to connection to arduino, there is no file: /dev/ttyACM0 {e}')
else:
    logger.error(f'Else step Arduino')


def main():
    logger.debug(f'Start main script')

    while(True):
        cow_id = pcf.Connect_RFID_reader()         
        if cow_id != '435400040001':                            # Comparision to null cow_id answer 
            logger.info("After read cow ID :", cow_id)
            weight_finall = pcf.Connect_ARD_get_weight(cow_id, s, type_scales) # Grab weight from arduino and collect to weight_finall
            logger.info("main: weight_finall", weight_finall)
                        
            if str(weight_finall) > '0':
                logger.info("main: Send data to server")
                pcf.Send_data_to_server(cow_id, weight_finall, type_scales) # Send data to server by JSON post request

main()