#!/usr/bin/python3

"""File containing all working functions and algorithm for spraying an animal.
Author: Suieubayev Maxat
Contact: maxat.suieubayev@gmail.com
Number: +7 775 818 48 43"""

import requests
from requests.exceptions import HTTPError
import RPi.GPIO as GPIO
import timeit
import json
from loguru import logger
import _config as cfg


def __spray_gpio_off(values) -> bool:  # Pump turn off function
    try:
        logger.info(f"Start spray_gpio_off")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        GPIO.setup(int(values.pin), GPIO.OUT)
        GPIO.output(int(values.pin), GPIO.LOW)
        GPIO.cleanup()
        spray_post = 'https://smart-farm.kz:8502/api/v2/SprayingTaskResults'  # url for post final data
        headers = {'Content-type': 'application/json'}  # headers for post data
        position = False
        end_time = timeit.default_timer()
        values.new_volume = (end_time - values.drink_start_time) * 8.3  # calculation of poured liquid
        post_data = __spray_json_payload(values)  # Dict for post to server
        post_res = requests.post(spray_post, data=json.dumps(post_data), headers=headers, timeout=3)
        logger.info(f'Post status code {post_res.status_code}')
        logger.info(f'GPIO is off. Pin number is {values.pin}')
        return position
    except Exception as e:
        logger.error(f"Error: Spray_GPIO_off function isn't work {e}")


def __spray_gpio_on(values) -> bool:    # Pump turn on function
    try:
        logger.info(f'Start spray gpio on')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        GPIO.setup(int(values.pin), GPIO.OUT)
        GPIO.output(int(values.pin), GPIO.HIGH)
        logger.info(f'Pump turn on is successful. Pin number is {values.pin}')
        return True
    except Exception as e:
        logger.error(f"Error: GPIO_on function isn't work {e}")
        position = __spray_gpio_off(values)
        return position


def __spray_json_payload(values) -> dict:  # Data collection in json
    try:
        logger.debug(f"Start spray_json_payload function")
        data = {
            "EventDate": '2024-07-04T09:51:35.046Z',
            "TaskId": values.task_id,
            "ScalesSerialNumber": values.type_scales,
            "SpayerSerialNumber": "s01000001",
            "RFIDNumber": values.cow_id,
            "SprayingType": values.spraying_type,
            "Volume": values.new_volume
        }

        return data
    except Exception as e:
        logger.error(f"Error in __spray_json_payload func: {e}")


def __request_get(values):  # Get data from the server
    try:
        cow_id = values.cow_id
        type_scales = values.type_scales
        url = 'https://smart-farm.kz:8502/api/v2/Sprayings?scalesSerialNumber=' + type_scales + \
              '&animalRfidNumber=' + cow_id
        request_get = requests.get(url, timeout=5).json()
        return request_get
    except Exception as e:
        logger.error(f'request get func error {e}')


def __spray_json_get(request_get_json, values, get_object=0):  # Convert data from the server to class
    try:
        logger.info(f"Start spray_json_get")
        values.task_id = request_get_json[get_object]['TaskId']
        values.spraying_type = request_get_json[get_object]['SprayingType']
        values.volume = request_get_json[get_object]['Volume']
        values.server_time = request_get_json[get_object]['ServerTime']
        return values
    except BaseException as b:
        logger.error(f"__spray_json_get error: {b}")


def __spray(position, values) -> bool:  # Start spray function
    try:
        logger.info(f"Start spray")
        spray_time = values.volume / 8.3 # 50 / 6(сек) = 8.3
        values.spray_duration = values.drink_start_time + spray_time  # Convert volume to time
        if values.spray_duration >= timeit.default_timer():
            # logger.error(f'Time is {spray_duration} {timeit.default_timer()}')   
            logger.info(f'Position is {position}')
            if position is False:
                position = __spray_gpio_on(values)  # Turn on pump
                return position
            else:
                return position
        else:
            logger.info(f'TimeOff')
            position = __spray_gpio_off(values)  # Turn off pump
            return position
    except ValueError as err:
        logger.error(f'Other error occurred: {err}')
        position = __spray_gpio_off(values)
        return position


def __spray_timer(position, values) -> bool:  # That's need to check timer on the next iteration
    try:
        logger.info(f'Start Spray timer check function')
        if values.spray_duration >= timeit.default_timer():
            logger.info(f'Time is {values.spray_duration} {timeit.default_timer()}')
            # logger.info(f'Position is {position}')          
            if position is False:
                __spray_gpio_on(values)
                position = True
                return position
            else:
                return position
        else:
            logger.info(f'TimeOff')
            position = __spray_gpio_off(values)
            return position
    except ValueError as err:
        logger.error(f'Other error occurred: {err}')
        position = __spray_gpio_off(values)
        return position


def __spraying_type(values) -> int:  # To find GPIO pin by liquid
    try:
        logger.info(f'Spraying type funct start')
        #pin_list = asdict(Pin())
        if values.spraying_type == 0:
            return cfg.get_setting("Sprayer", "medicine_pin")
            #return pin_list.get(values.type_scales)[0]
        else:
            return cfg.get_setting("Sprayer", "paint_pin")
            #return pin_list.get(values.type_scales)[1]
    except Exception as e:
        logger.error(f'__spraying type func error: {e}')


def spray_main_function(position, values) -> bool:  # That's a main function
    try:
        logger.info(f"Start spray_main_function")
        if position is False:  # If pump is off
            request_get_json = __request_get(values)  # Get data from server
            logger.debug(f'JSON Request: {request_get_json}')
            if not request_get_json:  # If Data is null
                logger.info(f'No tasks there')
                values.flag = True
                return position  # Exit from main function
            else:  # If Data is not null
                values = __spray_json_get(request_get_json, values)  # Take a values from server
                values.pin = __spraying_type(values)  # Take a GPIO pin number
                values.drink_start_time = timeit.default_timer()
                logger.debug(f'Values is: {values}')
                position = __spray(position, values)  # Start spray
                return position  # Exit from main function
        else:  # If pump is on
            position = __spray_timer(position, values)  # Check a timer and make a choice
            return position  # Exit from main function

    except HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
        position = __spray_gpio_off(values)
        return position

    except Exception as err:
        logger.error(f'Other error occurred: {err}')
        position = __spray_gpio_off(values)
        return position


def gpio_state_check(position, values) -> bool:  # Check the pump when out of loop
    try:
        logger.info(f"Start gpio_state_check")
        if position is True:  # If pump is on
            position = __spray_gpio_off(values)  # Turn off pump
            return position  # Exit from function
        else:
            return position  # Exit from function
    except HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
        position = __spray_gpio_off(values)
        return position
    except Exception as err:
        logger.error(f'Other error occurred: {err}')
        position = __spray_gpio_off(values)
        return position


def new_start_timer(position, values):  # Update start time value
    try:
        logger.info(f'New start timer function')
        if position is True:  # If pump is on
            return values  # Exit from function
        else:  # if pump is off
            values.drink_start_time = timeit.default_timer()  # Update start time value
            return values  # Exit from function
    except ValueError as e:
        logger.error(f'New_start_timer function Error: {e}')
