#!/usr/bin/python3
import datetime
import adc_data as ADC
import statistics
import re
from loguru import logger 
from collections import Counter
#import adc_data as HX
import _config as cfg
import time
import threading
import queue
import sys

import serial 

def get_one_value():
    pass

def bytes_to_int(response):
    try:
        data = []
        for i in range(4):
            data.append(response[i] & 0xFF)
        value = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]
        return value
    except Exception as e:
        logger.error(f'Error bytes_to_int: {e}')


def read_arduino(size=1):
    port = cfg.get_setting("Parameters", "arduino_port")
    arduino = serial.Serial(port, 9600, timeout = 1)
    weights = []
    try:
        for i in range(size):
            arduino.write(b'2')
            response = arduino.read()
            print(response)
            if response:
                logger.info(f'Responce is {response}\n')
                weight = int.from_bytes(response, byteorder='big', signed=False)
                weights.append(weight)
            else: 
                raise Exception(f'Error: Timeout or Invalid response lenght')
        logger.debug(f'Array[{size}]: {weights}\n')
        arduino.close()
        return weights
    except serial.SerialException as e:
        logger.error(f'Error read_arduino: {e}')
        arduino.close()
    except Exception as e:
        logger.error(f'{e}')

def measure_weight(hx):
    try:
        weight_arr = []
        weight = hx.calc_mean()
        start_timedate = str(datetime.datetime.now())    
        next_time = time.time()+1
        while weight > 10:
            weight = hx.calc_mean()
            current_time = time.time()
            time_to_wait = next_time - current_time
            if time_to_wait < 0:
                weight_arr.append(Counter(hx.get_arr()).most_common(1)[0][0])
                next_time = time.time()+1
                logger.debug(f'Common filter weights: {weight_arr}')

        if not weight_arr:
            logger.error("Error, null weight list")
            return 0, [], ''
        
        weight_finall = statistics.median(weight_arr)
        logger.debug(f'{type(weight_finall)}, {type(weight_arr)}, {type(start_timedate)}')
        return weight_finall, weight_arr, start_timedate

    except Exception as e:
        logger.error(f'measure_weight Error: {e}')


def connect_ard_get_weight(s): # Connection to aruino through USB by Serial Port
    try:
        s.flushInput() 
        s.flushOutput()
        weight = (str(s.readline())) # Start of collecting weight data from Arduino
        weight_new = re.sub("b|'|\r|\n", "", weight[:-5]) # 35.55 
        weight_list = []
        start_timedate = str(datetime.datetime.now())        

        while (float(weight_new) > 10): # Collecting weight to array 
            weight = (str(s.readline())) # wait something from arduino 
            weight_new = re.sub("b|'|\r|\n", "", weight[:-5]) # convert data from ard
            weight_list.append(float(weight_new))
            logger.debug(f'{weight_list}')

        if not weight_list:
            logger.error("Error, null weight list")
            return 0, [], ''

        else:
            if len(weight_list) > 1: # Here must added check on weight array null value and one element array
                del weight_list[-1]
            weight_finall = statistics.median(weight_list)
            logger.debug(f'{type(weight_finall)}, {type(weight_list)}, {type(start_timedate)}')
            return weight_finall, weight_list, start_timedate

    except Exception as e:
        logger.error(f"Error connection to Arduino {e}")
    except TypeError as t:
        logger.error(f'Cannot unpack non-iterable NoneType object {t}')


def calibrate():
    try:
        logger.info('Start calibrate function')
        port = cfg.get_setting("Parameters", "arduino_port")
        arduino = ADC.ArduinoSerial(port, 9600)
        logger.info(f"Remove any items from scale. Press any key when ready.")

        input()
        offset = arduino.calib_read()
        logger.info("Value at zero (offset): {}".format(offset))
        arduino.set_offset(offset)
        logger.info("Please place an item of known weight on the scale.")

        input()
        measured_weight = (arduino.calib_read()-arduino.get_offset())
        logger.info("Please enter the item's weight in kg.\n>")
        item_weight = input()
        scale = int(measured_weight)/int(item_weight)
        arduino.set_scale(scale)
        logger.info(f"Scale adjusted for kilograms: {scale}")
        logger.info(f'Offset: {offset}, set_scale(scale): {scale}')

        cfg.update_setting("Calibration", "Offset", offset)
        cfg.update_setting("Calibration", "Scale", scale)
        del arduino
        return offset, scale
    except:
        logger.error(f'calibrate Fail')
        cleanAndExit()


def __get_input(message, channel): # Функция для получения введенного значения
                                   # Ничего не менять!
    response = input(message)
    channel.put(response)


def input_with_timeout(message, timeout):   # Функция создания второго потока.
                                            # Временная задержка во время которой можно ввести значение
                                            # Ничего не менять!
    channel = queue.Queue()
    message = message + " [{} sec timeout] ".format(timeout)
    thread = threading.Thread(target=__get_input, args=(message, channel))
    thread.daemon = True
    thread.start()

    try:
        response = channel.get(True, timeout)
        return response
    except queue.Empty:
        pass
    return None


def calibrate_or_start():
    try:
        logger.info(f'("[1] to calibrate\n" "[2] to start measure\n>")')
        choice = '2'
        choice = input_with_timeout("Choice:", 5)
        time.sleep(5)

        if choice == '1':
            offset, scale = calibrate()
            cfg.update_setting("Calibration", "Offset", offset)
            cfg.update_setting("Calibration", "Scale", scale)

    except Exception as e:
        logger.error(f'Calibrate or start Error: {e}')


def cleanAndExit():
    logger.info("Cleaning up...")
    GPIO.cleanup()
    logger.info("Bye!")
    sys.exit()
        
