from datetime import datetime, date, time
import serial
import time
import socket
import json
import requests
import binascii
import csv
import re
#import pandas as pd # библиотека для записи массива в CSV файл

def Connect_ARD_get_weight(cow_id, s): # подключение к ардуино по сути чтение данных с последовательного порта  
    try:     
        weight = (str(s.readline()))
        
        weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
        print(weight_new)

        weight_list = []
        mid_weight = 0
        while (float(weight_new) != 0): # Collecting weight to array 
            weight = (str(s.readline()))
            print("Weight :", weight)
            weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
            print("Substracted weight: ", weight_new)
            #float(weight_new)
            weight_list.append(float(weight_new))
        if weight_list == 0 or weight_list == []:
            return(0)
        else:
            if weight_list != 0: # Здесь в будущем нужно добавить поверку на массив из одного элемента
                del weight_list[-1]
            weight_finall = sum(weight_list) / len(weight_list) 

            # Часть кода для записи массива в CSV файл сырых данных
            sep_line = "__________"
            if cow_id != "b'0700010101001e4b'":            
                with open('raw_data.csv', 'a+', newline='') as csvfile:
                    wtr = csv.writer(csvfile)
                    wtr.writerow([sep_line])
                    wtr.writerow([cow_id])
                    wtr.writerow([datetime.now()])
                    for x in weight_list : wtr.writerow ([x])
                csvfile.close()
            # конец части кода записи сырых данных
            
            print("Finish of the collect data")
            
            weight_list = []
            return(float(weight_finall))
    except Exception as e:
        print(e)
        print("Ошибка подключения к Ардуино 1")
    else:
        print("1 step rfid")

def Connect_RFID_reader(): # подключение к считывателю через TCP получение ID коровы формат str
    try:    
        ###########################################
        # TCP connection settings and socket
        TCP_IP = '192.168.1.250' #chafon 5300 reader address
        TCP_PORT = 60000 #chafon 5300 port
        BUFFER_SIZE = 1024

        animal_id = "b'0700010101001e4b'" # Id null starting variable
        animal_id_new = "b'0700010101001e4b'"
        null_id = "b'0700010101001e4b'" # Id null

        print("Connect RFID state")
        

        if animal_id == null_id: # Send command to reader waiting id of animal
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            #s.send(bytearray([0x06, 0x00, 0x01, 0x04, 0xff, 0xd4, 0x39])) # Chafon RU6403 reading command
            s.send(bytearray([0x53, 0x57, 0x00, 0x03, 0xff, 0xe0, 0x74])) #Chafon RU5300 reading mode command
            data = s.recv(BUFFER_SIZE)
            animal_id= str(binascii.hexlify(data))
            print("Received ID cow: ")
            print(animal_id)
            
            animal_id_new = animal_id[:-7] #Cutting the string from unnecessary information after 7 signs 
            animal_id_new = animal_id_new[-24:] #Cutting the string from unnecessary information before 24 signs
            
            print("CUT ID cow: ")
            print(animal_id_new)
                    
            s.close()             
        if animal_id_new == null_id: # Id null return(0)
            Connect_RFID_reader()
        else: # Id checkt return(1)
            animal_id = "b'0700010101001e4b'"
            return(animal_id_new)
    except Exception as e:
        print(e)
        print("Ошибка подключения к RFID reader")
    else: 
        print ("2 step RFID")
    
def Send_data_to_server(animal_id, weight_finall, type_scales): # Отправка данных на сервер КАТУ по JSON
    try:        
        print("Sending DATA TO SERVER:")
        #url = ('http://87.247.28.238:8501/api/weights')
        url = ('http://194.4.56.86:8501/api/weights')
        headers = {'Content-type': 'application/json'}
        data = {"AnimalNumber" : animal_id,
                "Date" : str(datetime.now()),
                "Weight" : weight_finall,
                "ScalesModel" : type_scales}
    except Exception as e:
        print(e)
        print("Ошибка передачи данных на сервер")
    else:
        print ("4 step send data")
        print ("End of the cycle")  

        #answer = requests.post(url, data=json.dumps(data), headers=headers)
        #try: 
        #    answer = requests.post(url, data=json.dumps(data), headers=headers)
        #except expression as identifier:
        #    print(expression)
            
        #print("RESULT:",answer)
        #response = answer.json()
        #print(response)


def Collect_data_CSV(cow_id, weight_finall, type_scales): # Запись данный в CSV файл по хорошему будет в sqlite
        
    try:        
        date_now = (str(datetime.now()))
        row = [cow_id, weight_finall,  date_now, type_scales]
        with open('cows_database.csv', 'a', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(row)
        writeFile.close()
    except Exception as e:
        print(e)
        print("Ошибка записи данных в файл")
    else:
        print ("3 step collect data")   

        weight_finall = 0 


#def spray_func(spray_period) # Команда опрыскивания коровы. Запрос в базу и чекание
    #GPIO.setmode(GPIO.BOARD)
    #GPIO.setup(22, GPIO.OUT)
    #GPIO.setup(22, GPIO.OUT, GPIO.LOW)
    # подключение к базе
    # проверка данных да/нет
    #if spray_period/next_spray_time != 0
    # опрыскивание (GPIO вывод сигнала)
    #GPIO.output(22, TRUE)
    #delay()
    #return()

#def delay_wait() # Может быть пригодится
