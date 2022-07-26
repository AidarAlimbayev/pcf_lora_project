#######################################################################################################################
"""
Основной код в full_spray.py. В файле full_spray_ru.py разбор кода.
Данная библиотека предназначена для опрыскивания.
Для того подключить библиотеку нужно сохранить 
файл full_spray.py в папку с основным кодом (lib_pcf.py). 
Импортировать библиотеку как spr (import full_spray as spr).
В функцию Connect_ARD_get_weight, в цикл while после всех функции 
добавить строки: 
gpio_state = spr.spray_main_function(spray_start_time, type_scales, scales_list, spray_get_url, cow_id, gpio_state)
spray_start_time = spr.new_start_timer(spray_start_time, gpio_state)
А также нужно добавить после цикла while строку проверки:
gpio_state = spr.gpio_state_check(scales_list, spray_start_time, spray_get_url, type_scales, cow_id, gpio_state)  
Если не совсем понятно, в конце файла пример.
Автор: Суйеубаев Максат Жамбылович
Контакты: +7 775 818 48 43, maxat.suieubayev@gmail.com"""
import requests                                         # Подключение библиотеки для общения с сервером
from requests.exceptions import HTTPError               # Библиотека для обработки ошибок сервера
import RPi.GPIO as GPIO                                 # Библиотека для работы с выводами Распберри
import timeit                                           # Библиотека для определения текущего времени
import json                                             # Библиотека для работы с json форматом

#########################################################################################################################

"""Функция включения насоса"""
#########################################################################################################################
def spray_gpio_on(pin):
    try:
        GPIO.setmode(GPIO.BOARD)                        # Выбор нумерации пинов (Board)
        GPIO.setwarnings(True)
        GPIO.setup(pin, GPIO.OUT)                       # Установка вывода распберри
        GPIO.output(pin, GPIO.HIGH)                     # Включаем насос
        # print_log(f"Start spray_gpio_on")                 # Раскомментить для теста 
        # print_log(f'GPIO is on. Pin number is {pin}')     # Раскомментить для теста
        return 0
    except Exception as e:
        print_log(f"Error: GPIO_on function isn't work {e}")        
#########################################################################################################################

"""Функция отключения насоса"""
#########################################################################################################################
def spray_gpio_off(pin):
    try:
        print_log(f"Start spray_gpio_off")
        GPIO.setmode(GPIO.BOARD)                        # Выбор нумерации пинов (Board)
        GPIO.setwarnings(True)
        GPIO.setup(pin, GPIO.OUT)                   
        GPIO.output(pin, GPIO.LOW)                      # Отключаем насос
        GPIO.cleanup()                                  # Очистка всех выводов распберри
        # print_log(f'GPIO is off. Pin number is {pin}')    # Раскомментить для теста 
        return 0
    except Exception as e:
        print_log(f"Error: Spray_GPIO_off function isn't work {e}")        
#########################################################################################################################

"""Функция подготовки json строки для отправки на сервер"""
#########################################################################################################################
def spray_json_payload(server_time, task_id, new_volume, spraying_type, scales_type, animal_id):
    try:
        # print_log(f"Start spray_json_payload")              # Раскомментить для теста 
        data = {
            "EventDate": server_time,                   # Переменная серверного времени
            "TaskId": task_id,                          # Переменная номера задания
            "ScalesSerialNumber": scales_type,          # Переменная модели весов
            "SpayerSerialNumber": "s01000001",          # Переменная номера опрыскивателя
            "RFIDNumber": animal_id,                    # Переменная RFID животного
            "SprayingType": spraying_type,              # Переменная типа жидкости
            "Volume": new_volume                        # Переменная опрыснутого объема
            }
        return data
    except Exception as e:
        print_log(f"Something wrong {e}")
#########################################################################################################################

"""Функция для получения информации из сервера и записи данных в переменные"""
#########################################################################################################################
def spray_json_get(url, get_object):
    try:
        # print_log(f"Start spray_json_get")                # Раскомментить для теста 
        task_id = requests.get(url).json()[get_object]['TaskId']
        spraying_type = requests.get(url).json()[get_object]['SprayingType']
        volume = requests.get(url).json()[get_object]['Volume']
        server_time = requests.get(url).json()[get_object]['ServerTime']
        # print_log(requests.get(url).json())               # Раскомментить для теста 
        return task_id, spraying_type, volume, server_time
    except ValueError:
        print_log(f"Something wrong")
#########################################################################################################################

"""Функция опрыскивания"""
#########################################################################################################################
def spray(start_time, position, pin, server_time, task_id, volume, spraying_type, scales_type, animal_id):
    try:
        # print_log(f"Start spray")                           # Раскомментить для теста 
        spray_post = 'https://smart-farm.kz:8502/api/v2/SprayingTaskResults'
        headers = {'Content-type': 'application/json'}
        spray_time = volume / 8.3                       # Определение продолжительности опрыскивания
        spray_duration = start_time + spray_time        # Продолжительность + настоящее время = ПНВ
        if spray_duration >= timeit.default_timer():    # Если ПНВ больше или равно настоящего времени
            # print_log(f'Time is {spray_duration} {timeit.default_timer()}')   # Раскомментить для теста 
            # print_log(f'Position is {position}')          # Раскомментить для теста 
            if position is False:                       # Если насос отключен
                spray_gpio_on(pin)                      # Включить насос
                position = True                         # Флаг состояния насоса
                return position                         # Возвращаем флаг
            else:
                return position                         # Возвращаем флаг
        else:                                           # Если ПНВ меньше настоящего времени
            # print_log(f'TimeOff')                         # Раскомментить для теста 
            spray_gpio_off(pin)                         # Выключаем насос
            position = False                            # Флаг состояния насоса
            end_time = timeit.default_timer()           # Время окончания
            new_volume = (end_time - start_time) * 8.3  # Новый объем
            """Записываем весь вывод данных в json post_data"""
            post_data = spray_json_payload(server_time, task_id, new_volume, spraying_type, scales_type, animal_id)
            """Записываем что и куда передать post_res"""
            post_res = requests.post(spray_post, data=json.dumps(post_data), headers=headers, timeout=0.25)
            # print_log(f"Post_res result, {post_res}")       # Раскомментить для теста 
            # print_log(post_res.raise_for_status())          # Раскомментить для теста 
            return position                             # Возвращаем флаг
    except ValueError as err:
        print_log(f'Other error occurred: {err}')
#########################################################################################################################

"""Основная функция опрыскивания. Подключать в цикл while."""
#########################################################################################################################
def spray_main_function(start_time, scales_type, pin_list, spray_get, animal_id, position):
    try:
        # print_log(f"Start spray_main_function")         # Раскомментить для теста 
        if not requests.get(spray_get, timeout=0.5).json():        # Если приходит пустой ответ
            # print_log(f'No tasks there')                # Раскомментить для теста 
            return position                         # Возвращаем флаг      
        else:
            """Вытаскиваем все переменные из ответа от сервера"""
            task_id, spraying_type, volume, server_time = spray_json_get(spray_get, 0)
            if spraying_type == 0:                  # Если тип опрыскивания препарат то 
                """Из массива scales_list получаем пин для опрыскивания лекарством на данных весах"""
                pin = pin_list.get(scales_type)[0]
                """Вызываем функцию опрыскивания"""
                position = spray(start_time, position, pin, task_id, spraying_type, volume, server_time, scales_type, animal_id)
                return position                     # Возвращаем флаг

            else:                                   # Если тип опрыскивания окрашивание то 
                """Из массива scales_list получаем пин для опрыскивания лекарством на данных весах"""
                pin = pin_list.get(scales_type)[1]
                """Вызываем функцию опрыскивания"""
                position = spray(start_time, position, pin, task_id, spraying_type, volume, server_time, scales_type, animal_id)
                return position                     # Возвращаем флаг

    except HTTPError as http_err:
        print_log(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print_log(f'Other error occurred: {err}')
#########################################################################################################################

"""Функция проверки состояния насоса. Подключать после основного цикла while."""
#########################################################################################################################
def gpio_state_check(pin_list, start_time, spray_get, scales_type, animal_id, position):
    try:
        # print_log(f"Start gpio_state_check")            # Раскомментить для теста 
        spray_post = 'https://smart-farm.kz:8502/api/v2/SprayingTaskResults'
        headers = {'Content-type': 'application/json'}
        if position is True:                          # Если насос влючен 
            task_id, spraying_type, volume, server_time = spray_json_get(spray_get, 0)
            if spraying_type == 0:                    # Если опрыскиваем препаратом то
                """Из массива scales_list получаем пин для опрыскивания лекарством на данных весах"""
                pin = pin_list.get(scales_type)[0]    # Забираем пин препарата
                """Вызываем функцию опрыскивания"""
            else:                                     # Если опрыскиваем краской то
                """Из массива scales_list получаем пин для опрыскивания лекарством на данных весах"""
                pin = pin_list.get(scales_type)[1]    # Забираем пин краски
            spray_gpio_off(pin)                       # Выключаем насос
            end_time = timeit.default_timer()         # Время отключения 
            new_volume = (end_time - start_time) * 8.3  # Объем фактически вылитой жидкости
            """ Собираем данные в json строку """
            post_data = spray_json_payload(server_time, task_id, int(new_volume), spraying_type, scales_type, animal_id)
            """ Отправляем данные на сервер """
            post_res = requests.post(spray_post, data=json.dumps(post_data), headers=headers)
            # print_log(post_res.raise_for_status())      # Раскомментить для теста 
            position = False                        # Флаг отключенного насоса
            
            return position                         # Возвращаем флаг насоса
        else:                                       # Если насос отключен
            return position                         # Возвращаем флаг насоса

    except HTTPError as http_err:
        print_log(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print_log(f'Other error occurred: {err}')
#########################################################################################################################

"""Функция запуска нового таймера"""
#########################################################################################################################
def new_start_timer(start_time, position):
    try:
        if position is True:                        # Если насос влючен
            return start_time                       # Возвращаем время 
        else:                                       # Если насос отключен
            start_time = timeit.default_timer()     # Переменная нового таймера
            return start_time                       # Возвращаем новое время
    except ValueError as e:
        print_log(f'New_start_timer function Error: {e}')
#########################################################################################################################

"""Пример подключения библиотеки в основной код. Ориентир #!"""
#########################################################################################################################
"""def Connect_ARD_get_weight(cow_id, type_scales): # Connection to aruino through USB by Serial Port
    try:
        #!scales_list = {'01000001': [11, 10],
                       'scales_model_5': [21, 22],gpio_state = spray_main_function(drink_start_time, type_scales, scales_list, spray_get_url, cow_id, gpio_state)
                       'scales_model_6': [33, 32],
                       'scales_model_7': [44, 43],
                       'scales_model_10': [55, 54], 
                       'pcf_1_model_1_80': [13, 50]}
        #!spray_get_url = 'https://smart-farm.kz:8502/api/v2/Sprayings?scalesSerialNumber='+type_scales+'&animalRfidNumber='+cow_id
        #!gpio_state = False
        
        
        #!spray_start_time = timeit.default_timer()


        while (float(weight_new) > 10): # Collecting weight to array  
            #!gpio_state = spray_main_function(spray_start_time, type_scales, scales_list, spray_get_url, cow_id, gpio_state)
            #!spray_start_time = new_start_timer(spray_start_time, gpio_state)
        
        
        #After while    
        #!gpio_state = gpio_state_check(scales_list, spray_start_time, spray_get_url, type_scales, cow_id, gpio_state) 

    except Exception as e:
        print_log("Error connection to Arduino", e)
#########################################################################################################################
"""


