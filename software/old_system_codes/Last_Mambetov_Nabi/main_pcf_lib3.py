from datetime import datetime, date, time
import serial
import time
import socket
import json
import requests
import binascii
import csv
import re
import logging

logging.basicConfig(filename = '%s.log'%str(datetime.now()), level = logging.DEBUG, format='%(asctime)s %(message)s')

def Connect_ARD_get_weight(cow_id, s): # Connection to aruino through USB by Serial Port   
    try:
        s.flushInput() # Cleaning buffer of Serial Port
        s.flushOutput() # Cleaning output buffer of Serial Port
        logging.info('lib: Con_ARD: connect arduino after flush')
        logging.info(s)
        logging.info('lib: Con_ARD: connect arduino s.name fuction answer:')
        logging.info(s.name)
        print("lib:Con_ARD: Start collect weight")
        logging.info("lib:Con_ARD: Start collect weight")

        weight = (str(s.readline())) # Start of collecting weight data from Arduino
        logging.info("lib:Con_ARD: Start collect weight")
        logging.info(weight)
        logging.info("lib:Con_ARD: after s.readline function")

        weight_new = re.sub("b|'|\r|\n", "", weight[:-5])

        print("lib:Con_ARD: weight new: ")
        print(float(weight_new))
        logging.info("lib:Con_ARD: weight new: ")
        logging.info(float(weight_new))
        
        weight_list = []
        mid_weight = 0
        while (float(weight_new) > 10): # Collecting weight to array 
            weight = (str(s.readline()))
            weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
            print("weight from Arduino: ")
            print(weight_new)
            logging.info("lib:Con_ARD: weight from arduino: ")
            logging.info(weight_new)
            weight_list.append(float(weight_new))
        if weight_list == 0 or weight_list == []:
            return(0)
        else:
            if weight_list != []: # Here must added check on weight array null value and one element array
                del weight_list[-1]
            weight_finall = sum(weight_list) / len(weight_list) # Averaging weight array by sum and lenght
            #weight_finall = weight_finall/1000 # Dividing to 1000 for Igor's server  
            logging.info("lib:Con_ARD: weight_finall new: ")
            logging.info("{0:.2f}".format(weight_finall))
            # Part of code to save all raw data into CSV file
            sep_line = "__________"
            if cow_id != "b'0700010101001e4b'":            
                with open('raw_data.csv', 'a+', newline='') as csvfile:
                    wtr = csv.writer(csvfile)
                    wtr.writerow([sep_line])
                    wtr.writerow([cow_id])
                    wtr.writerow([datetime.now()])
                    for x in weight_list : wtr.writerow ([x])
                    logging.info("lib: weight_list: ")
                    logging.info(weight_list)
                csvfile.close()
            logging.info("lib:Con_ARD:End of write raw data list: ")
            logging.info(weight_list)
            # End of collectin raw data into CSV file
                        
            weight_list = []
            return(float("{0:.2f}".format(weight_finall)))
    except Exception as e:
        logging.info("lib: Con_ARD: Err connection to Arduino")
        logging.info(e)
    else:
        print("lid:RFID_reader: 1 step")
        logging.info("lid:RFID_reader: 1 step")

def Connect_RFID_reader(): # Connection to RFID Reader through TCP and getting cow ID in str format
    try:    
        print("lib:RFID_reader: Start RFID Function")
        logging.info("lib:RFID_reader: Start RFID Function")
        ###########################################
        # TCP connection settings and socket
        TCP_IP = '192.168.1.250' #chafon 5300 reader address
        TCP_PORT = 60000 #chafon 5300 port
        BUFFER_SIZE = 1024
        animal_id = "b'0700010101001e4b'" # Id null starting variable
        animal_id_new = "b'0700010101001e4b'"
        null_id = "b'0700010101001e4b'" # Id null
    
        if animal_id == null_id: # Send command to reader waiting id of animal
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(bytearray([0x53, 0x57, 0x00, 0x06, 0xff, 0x01, 0x00, 0x00, 0x00, 0x50])) #Chafon RU5300 Answer mode reading mode command
            data = s.recv(BUFFER_SIZE)
            animal_id= str(binascii.hexlify(data))
            animal_id_new = animal_id[:-5] #Cutting the string from unnecessary information after 7 signs 
            animal_id_new = animal_id_new[-12:] #Cutting the string from unnecessary information before 24 signs
            logging.info("lib:RFID_reader: new ID: ")
            logging.info(animal_id_new)
            s.close()             
        if animal_id_new == null_id: # Id null return(0)
            Connect_RFID_reader()
        else: # Id checkt return(1)
            animal_id = "b'0700010101001e4b'"
            logging.info("lib:RFID_reader: Success step 2 RFID")
            return(animal_id_new)
    except Exception as e:
        logging.info("lib:RFID_reader: Err connect to Arduino ")
        logging.info(e)
    else: 
        logging.info("lib:RFID_reader: 2 step RFID")
    
def Send_data_to_server(animal_id, weight_finall, type_scales): # Sending data into Igor's server through JSON
    try:
        print("lib:RFID_reader: Start sending DATA TO SERVER:")
        logging.info("lib:RFID_reader: Start sending DATA TO SERVER:")
        url = 'http://194.4.56.86:8501/api/weights'
        headers = {'Content-type': 'application/json'}
        data = {"AnimalNumber" : animal_id,
                "Date" : str(datetime.now()),
                "Weight" : weight_finall,
                "ScalesModel" : type_scales}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        logging.info("lib:RFID_reader: Answer from server: ")
        logging.info(answer) # Is it possible to stop on this line in the debug?
        logging.info("Content of answer from server")
        logging.info(answer.content)
        print("lib:RFID_reader: Answer from server: ")
        print(answer)
        print("Content of answer from server")
        print(answer.content)
    except Exception as e:
        logging.info("lib:RFID_reader: Err send data to server")
        logging.info(e)
    else:
        logging.info("lib:RFID_reader: 4 step send data")
        logging.info("lib:RFID_reader: End of the cycle")  

def Collect_data_CSV(cow_id, weight_finall, type_scales): # Collocting datat into CSV, in the future must be in SQLite
    try:
        print("lib:CSV_data: Start write to file")
        logging.info("lib:CSV_data: Start write to file")
        date_now = (str(datetime.now()))
        row = [cow_id, weight_finall,  date_now, type_scales]
    
        with open('cows_database.csv', 'a', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(row)
        writeFile.close()
    except Exception as e:
        logging.info("lib:CSV_data: Err to write file")
    else:
        logging.info("lib:CSV_data: 3 step collect data")   


#def spray_func(spray_period) # Function to spray cow. Request to database and check from database 
    #GPIO.setmode(GPIO.BOARD)
    #GPIO.setup(22, GPIO.OUT)
    #GPIO.setup(22, GPIO.OUT, GPIO.LOW)
    # Conncection to database
    # Checking Yes or No about previous spraying action 
    #if spray_period/next_spray_time != 0
    # Spray action (GPIO Signal output)
    #GPIO.output(22, TRUE)
    #delay()
    #return()

#def delay_wait() # Maybe required later
