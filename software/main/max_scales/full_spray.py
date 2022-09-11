from cmath import pi
from urllib import request
import requests                                         
from requests.exceptions import HTTPError               
import RPi.GPIO as GPIO                                 
import timeit                                           
import json      
from loguru import logger                                       
########################################################


########################################################
logger.add('scales.log', format="{time} {level} {message}", 
level="DEBUG", rotation="1 day", compression="zip") #serialize="True")

pin = 0
spray_duration = 0
server_time = ''
task_id = 0
volume = 0
spraying_type = 0
spray_post = 'https://smart-farm.kz:8502/api/v2/SprayingTaskResults'
headers = {'Content-type': 'application/json'}


def __spray_gpio_off(pin, scales_type, animal_id, start_time):
    try:
        # logger.error(f"Start spray_gpio_off")
        GPIO.setmode(GPIO.BOARD)                        
        GPIO.setwarnings(True)
        GPIO.setup(pin, GPIO.OUT)                   
        GPIO.output(pin, GPIO.LOW)                      
        GPIO.cleanup()
        position = False                            
        end_time = timeit.default_timer()           
        new_volume = (end_time - start_time) * 8.3  
        post_data = __spray_json_payload(server_time, task_id, new_volume, spraying_type, scales_type, animal_id)
        post_res = requests.post(spray_post, data=json.dumps(post_data), headers=headers, timeout=0.5)                                  
        # logger.error(f 'GPIO is off. Pin number is {pin}')
        return position
    except Exception as e:
        logger.error(f"Error: Spray_GPIO_off function isn't work {e}")     
########################################################


########################################################
def __spray_gpio_on(pin, scales_type, animal_id, start_time):
    try:
        GPIO.setmode(GPIO.BOARD)                        
        GPIO.setwarnings(True)
        GPIO.setup(pin, GPIO.OUT)                       
        GPIO.output(pin, GPIO.HIGH)                     
        # logger.error(f"Start spray_gpio_on")                  
        # logger.error(f'GPIO is on. Pin number is {pin}')     
        return 0
    except Exception as e:
        logger.error(f"Error: GPIO_on function isn't work {e}")   
        position = __spray_gpio_off(pin, scales_type, animal_id, start_time)  
        return position     
########################################################


########################################################
def __spray_json_payload(new_volume, scales_type, animal_id, pin, start_time):
    try:
        # logger.error(f"Start spray_json_payload")               
        data = {
            "EventDate": server_time,                   
            "TaskId": task_id,                          
            "ScalesSerialNumber": scales_type,          
            "SpayerSerialNumber": "s01000001",          
            "RFIDNumber": animal_id,                    
            "SprayingType": spraying_type,              
            "Volume": new_volume                        
            }
        return data
    except Exception as e:
        logger.error(f"Something wrong {e}")
        position = __spray_gpio_off(pin, scales_type, animal_id, start_time)  
        return position
########################################################


########################################################
def __request_get(url):
    try:
        request_get = requests.get(url, timeout=0.5).json
        return request_get
    except Exception as e:
        logger.error(f'request get func error {e}')
########################################################


########################################################
def __spray_json_get(request_get_json, get_object=0):
    try:
        logger.info(f"Start spray_json_get")                        
        task_id_get = request_get_json[get_object]['TaskId']
        spraying_type_get = request_get_json[get_object]['SprayingType']
        volume_get = request_get_json[get_object]['Volume']
        server_time_get = request_get_json[get_object]['ServerTime']
        return task_id_get, spraying_type_get, volume_get, server_time_get
    except BaseException as b:
        logger.error(f"__spray_json_get error: {b}")
########################################################


########################################################
def __spray(start_time, position, pin, vol, scales_type, animal_id):
    try:
        logger.info(f"Start spray")                           
        spray_time = vol / 8.3
        spray_duration = start_time + spray_time        
        if spray_duration >= timeit.default_timer():    
            # logger.error(f'Time is {spray_duration} {timeit.default_timer()}')   
            logger.info(f'Position is {position}')          
            if position is False:                       
                __spray_gpio_on(pin)                      
                position = True                         
                return spray_duration, position
            else:
                return spray_duration, position
        else:                                           
            logger.info(f'TimeOff')                         
            position = __spray_gpio_off(pin, scales_type, animal_id, start_time)                                 
            return position                             
    except ValueError as err:
        logger.error(f'Other error occurred: {err}')
        position = __spray_gpio_off(pin, scales_type, animal_id, start_time)  
        return position
########################################################


########################################################
def __spray_timer(spray_duration, position, pin, scales_type, animal_id, start_time):
    try:
        if spray_duration >= timeit.default_timer():    
            # logger.info(f'Time is {spray_duration} {timeit.default_timer()}')   
            # logger.info(f'Position is {position}')          
            if position is False:                       
                __spray_gpio_on(pin)                      
                position = True                         
                return position                         
            else:
                return position                         
        else:                                           
            logger.info(f'TimeOff')                         
            position = __spray_gpio_off(pin, scales_type, animal_id, start_time)                                 
            return position                             
    except ValueError as err:
        logger.error(f'Other error occurred: {err}')
        position = __spray_gpio_off(pin, scales_type, animal_id, start_time)  
        return position
########################################################


########################################################
def __spraying_type(spraying_type, pin_list, scales_type):
    try:
        if spraying_type == [0]: return pin_list.get(scales_type)[0]         
        else: return pin_list.get(scales_type)[1]
         
    except Exception as e:
        logger.error(f'__spraying type func error: {e}')
########################################################


########################################################
def spray_main_function(start_time, scales_type, pin_list, spray_get, animal_id, spray_duration, position):
    try:
        logger.info(f"Start spray_main_function")   
        if position is False:
            request_get_json = __request_get(spray_get)
            if request_get_json is []:
                logger.info(f'No tasks there')
                return position
            else: 
                task_id, spraying_type, volume, server_time = __spray_json_get(request_get_json)
                pin = __spraying_type(spraying_type, pin_list, scales_type)
                spray_duration, position = __spray(start_time, position, pin, volume, server_time, scales_type, animal_id)
                return spray_duration, position   
        else:
            position = __spray_timer(spray_duration, position, pin, scales_type, animal_id, start_time)
            return position

    except HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
        position = __spray_gpio_off(pin, scales_type, animal_id, start_time)  
        return position
        
    except Exception as err:
        logger.error(f'Other error occurred: {err}')
        position = __spray_gpio_off(pin, scales_type, animal_id, start_time)  
        return position
########################################################


########################################################
def gpio_state_check(pin_list, start_time, spray_get, scales_type, animal_id, position):
    try:
        # logger.error(f"Start gpio_state_check")            
        
        if position is True:                          
            task_id, spraying_type, volume, server_time = __spray_json_get(spray_get, 0)
            if spraying_type == 0:                    
                pin = pin_list.get(scales_type)[0]    
            else:                                     
                pin = pin_list.get(scales_type)[1]    
            __spray_gpio_off(pin, scales_type, animal_id, start_time)                        
            end_time = timeit.default_timer()          
            new_volume = (end_time - start_time) * 8.3  
            post_data = __spray_json_payload(server_time, task_id, int(new_volume), spraying_type, scales_type, animal_id)
            post_res = requests.post(spray_post, data=json.dumps(post_data), headers=headers)
            # logger.error(post_res.raise_for_status())      
            position = False                        
            return position                          
        else:                                       
            return position                          

    except HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
        position = __spray_gpio_off(pin, scales_type, animal_id, start_time)  
        return position
    except Exception as err:
        logger.error(f'Other error occurred: {err}')
        position = __spray_gpio_off(pin, scales_type, animal_id, start_time)  
        return position
########################################################


########################################################
def new_start_timer(start_time, position):
    try:
        if position is True:                        
            return start_time                       
        else:                                       
            start_time = timeit.default_timer()     
            return start_time                       
    except ValueError as e:
        logger.error(f'New_start_timer function Error: {e}')
########################################################