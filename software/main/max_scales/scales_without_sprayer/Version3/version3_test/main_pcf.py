#!/usr/bin/sudo python

"""Scales main file without sprayer. Version 5.1
by Alimbayev Aidar and Suieubayev Maxat."""

import _headers as hdr

requirement_list = ['loguru', 'requests', 'RPi.GPIO', 'numpy', 'pandas', 'matplotlib']
hdr.install_packages(requirement_list)

import software.main.max_scales.scales_without_sprayer.Version3.version3_test.lib_test as pcf
import time
import software.main.max_scales.scales_without_sprayer.Version3.version3_test.adc_data as HX
time.sleep(10)
import RPi.GPIO as GPIO 
from datetime import datetime, time
from loguru import logger
import _config as cfg

logger.add('log/scales_{time}.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")             #serialize="True")

type_scales = cfg.get_setting("Parameters", "feeder_type")
cow_id = "b'435400040001'"                                      # value of null answer of RFID reader
weight_finall = 0

logger.info(f'main: Start script')

@logger.catch
def main():
    try:
        logger.debug(f'Start main script')
        pcf.calibrate_or_start()
        while(True):

            cow_id = pcf.connect_rfid_reader()        
            if cow_id != '435400040001':                            # Comparision to null cow_id answer 
                GPIO.setmode(GPIO.BCM) 
                hx = HX.HX711(19, 26) # dt, sck
                GPIO.setwarnings(False)
                logger.info("After read cow ID :", cow_id)
                weight_finall, weight_array, weighing_start_time = pcf.measure_weight(hx) # Grab weight from arduino and collect to weight_finall
                logger.info("main: weight_finall", weight_finall)
                weighing_end_time = str(datetime.now())
                            
                if str(weight_finall) > '0':
                    logger.info("main: Send data to server")
                    pcf.post_array_data(type_scales, cow_id, weight_array, weighing_start_time, weighing_end_time)
                    pcf.post_median_data(cow_id, weight_finall, type_scales) # Send data to server by JSON post request
                GPIO.cleanup()
    except Exception as e:
        logger.error(f'Main Error: {e}')
        pcf.cleanAndExit()
main()