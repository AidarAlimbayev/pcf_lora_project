#!/usr/bin/sudo python

"""Scales main file without sprayer. Version 5.1
by Alimbayev Aidar and Suieubayev Maxat."""

import _headers as hdr

requirement_list = ['loguru', 'requests', 'RPi.GPIO', 'pyserial']
hdr.install_packages(requirement_list)

import lib_test as pcf
import time
#time.sleep(10)
from datetime import datetime, time
from loguru import logger
import _config as cfg


logger.add('log/scales_{time}.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip")             #serialize="True")

type_scales = cfg.get_setting("Parameters", "feeder_type")
logger.info(f'main: Test script')

@logger.catch
def main():
    try:
        logger.debug(f'Start main script')
        while(True):
            # logger.debug(f'Enter 1 to take adc value from arduino\n Enter 2 to exit')
            # choice = input()
            # if choice == 1:
                pcf.read_arduino(2)
            # else: 
            #     break
    except Exception as e:
        logger.error(f'Main Error: {e}')

main()