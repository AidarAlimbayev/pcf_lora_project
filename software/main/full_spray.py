import requests                                         
from requests.exceptions import HTTPError               
import RPi.GPIO as GPIO                                 
import timeit                                           
import json                                             
import logging
from datetime import datetime

########################################################

# name of log file as datetime of creation example: "2022-06-12_16_44_22.890654.log"
logging.basicConfig(filename = 'full_spray_%s.log'%str(datetime.now().strftime("%Y-%m-%d_%H_%M_%S")), level = logging.DEBUG, format='[%(filename)s:%(lineno)s - %(funcName)20s() ] %(asctime)s %(message)s')


###################################################################################################
# Pring log function, Insert first variable message in the second value of error
def print_log(message = None, value = None): # Function to logging and printing messages into terminal for debug
    logging.info(message)
    if value != None:
        logging.info(value)
    print(message)
    if value != None:
        print(value)
    return 0
###################################################################################################


########################################################
def spray_gpio_on(pin):
    try:
        GPIO.setmode(GPIO.BOARD)                        
        GPIO.setwarnings(True)
        GPIO.setup(pin, GPIO.OUT)                       
        GPIO.output(pin, GPIO.HIGH)                     
        print_log(f"Start spray_gpio_on")                  
        print_log(f'GPIO is on. Pin number is {pin}')     
        return 0
    except Exception as e:
        print_log(f"Error: GPIO_on function isn't work {e}")        
########################################################


########################################################
def spray_gpio_off(pin):
    try:
        print_log(f"Start spray_gpio_off")
        GPIO.setmode(GPIO.BOARD)                        
        GPIO.setwarnings(True)
        GPIO.setup(pin, GPIO.OUT)                   
        GPIO.output(pin, GPIO.LOW)                      
        GPIO.cleanup()                                  
        print_log(f'GPIO is off. Pin number is {pin}')    
        return 0
    except Exception as e:
        print_log(f"Error: Spray_GPIO_off function isn't work {e}")        
########################################################


########################################################
def spray_json_payload(server_time, task_id, new_volume, spraying_type, scales_type, animal_id):
    try:
        print_log(f"Start spray_json_payload")               

        data = {
            "EventDate": server_time,                   
            "TaskId": task_id,                          
            "ScalesSerialNumber": scales_type,          
            "SpayerSerialNumber": "s01000001",          
            "RFIDNumber": animal_id,                    
            "SprayingType": spraying_type,              
            "Volume": new_volume                        
            }
        print_log("Payload data return:", data)
        return data
    except Exception as e:
        print_log(f"Something wrong {e}")
########################################################


########################################################
def spray_json_get(url, get_object):
    try:
        print_log(f"Start spray_json_get")                
        task_id = requests.get(url).json()[get_object]['TaskId']
        spraying_type = requests.get(url).json()[get_object]['SprayingType']
        volume = requests.get(url).json()[get_object]['Volume']
        server_time = requests.get(url).json()[get_object]['ServerTime']
        print_log(requests.get(url).json())               
        print_log("In full_spray.py: def spray_json_get  | Task_Id ", task_id)
        print_log("In full_spray.py: def spray_json_get  | Server_Time :", server_time)

        return task_id, spraying_type, volume, server_time
    except ValueError:
        print_log(f"Something wrong")
########################################################


########################################################
def spray(start_time, position, pin, server_time, task_id, volume, spraying_type, scales_type, animal_id):
    try:
        print_log(f"Start spray")    
        print_log("In full_spray.py: def spray  | Task_Id ", task_id)

        print_log("In full_spray.py: def spray  | server_time :", server_time)                      
        spray_post = 'https://smart-farm.kz:8502/api/v2/SprayingTaskResults'
        headers = {'Content-type': 'application/json'}
        spray_time = volume / 8.3                       
        spray_duration = start_time + spray_time        
        if spray_duration >= timeit.default_timer():    
            print_log(f'Time is {spray_duration} {timeit.default_timer()}')   
            print_log(f'Position is {position}')          
            if position is False:                       
                spray_gpio_on(pin)                      
                position = True                         
                return position                         
            else:
                return position                         
        else:                                           
            print_log(f'TimeOff')                         
            spray_gpio_off(pin)                         
            position = False                            
            end_time = timeit.default_timer()           
            new_volume = (end_time - start_time) * 8.3  
            print_log("In full_spray.py: def spray  | Task_Id ", task_id)
            print_log("In full_spray.py: def spray  | server_time :", server_time)
            post_data = spray_json_payload(server_time, task_id, new_volume, spraying_type, scales_type, animal_id)
            post_res = requests.post(spray_post, data=json.dumps(post_data), headers=headers, timeout=1)
            print_log(f"Post_res result, {post_res}")       
            print_log(post_res.raise_for_status())          
            return position                             
    except ValueError as err:
        print_log(f'Other error occurred: {err}')
########################################################


########################################################
def spray_main_function(start_time, scales_type, pin_list, spray_get, animal_id, position):
    try:
        print_log(f"Start spray_main_function")         
        if not requests.get(spray_get, timeout=0.5).json():        
            print_log(f'No tasks there')                
            return position                              
        else:
            
            task_id, spraying_type, volume, server_time = spray_json_get(spray_get, 0)
            print_log("In full_spray.py : spray_main_function  Task_Id :", task_id)
            print_log("In full_spray.py : spray_main_function  Spraying_type :", spraying_type)
            print_log("In full_spray.py : spray_main_function  Volume :", volume)
            print_log("In full_spray.py : spray_main_function  server_time :", server_time)
            if spraying_type == 0:                  
                pin = pin_list.get(scales_type)[0]
                print_log("In full_spray.py : spray_main_function  Task_Id in Spraying type:", task_id)
                position = spray(start_time, position, pin, server_time, task_id, volume, spraying_type, scales_type, animal_id)
                return position                     

            else:                                  
                pin = pin_list.get(scales_type)[1]
                position = spray(start_time, position, pin, server_time, task_id, volume, spraying_type, scales_type, animal_id)
                return position                     

    except HTTPError as http_err:
        print_log(f'HTTP error occurred: {http_err}')
        spray_gpio_off(pin)
        position = False
        return position
    except Exception as err:
        print_log(f'Other error occurred: {err}')
        spray_gpio_off(pin)
        position = False
        return position
########################################################


########################################################
def gpio_state_check(pin_list, start_time, spray_get, scales_type, animal_id, position):
    try:
        print_log(f"Start gpio_state_check")            
        spray_post = 'https://smart-farm.kz:8502/api/v2/SprayingTaskResults'
        headers = {'Content-type': 'application/json'}
        if position is True:                          
            task_id, spraying_type, volume, server_time = spray_json_get(spray_get, 0)
            if spraying_type == 0:                    
                pin = pin_list.get(scales_type)[0]    
            else:                                     
                pin = pin_list.get(scales_type)[1]    
            spray_gpio_off(pin)                       
            end_time = timeit.default_timer()          
            new_volume = (end_time - start_time) * 8.3  
            post_data = spray_json_payload(server_time, task_id, int(new_volume), spraying_type, scales_type, animal_id)
            post_res = requests.post(spray_post, data=json.dumps(post_data), headers=headers, timeout=1)
            print_log(post_res.raise_for_status())      
            position = False                        
            return position                          
        else:                                       
            return position                          

    except HTTPError as http_err:
        print_log(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print_log(f'Other error occurred: {err}')
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
        print_log(f'New_start_timer function Error: {e}')
########################################################