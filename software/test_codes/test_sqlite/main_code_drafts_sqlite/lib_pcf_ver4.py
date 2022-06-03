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
import os
import statistics
import sqlite3 as sq3


#logging.basicConfig(filename = '%s.log'%str(datetime.now()), level = logging.DEBUG, format='%(asctime)s %(message)s')
#logging format with names of funstions
logging.basicConfig(filename = '%s.log'%str(datetime.now()), level = logging.DEBUG, format='[%(filename)s:%(lineno)s - %(funcName)20s() ] %(asctime)s %(message)s')


def print_log(message = None, value = None): # Function to logging and printing messages into terminal for debug
    logging.info(message)
    logging.info(value)
    print(message)
    print(value)


###################################################################################################
# Collect to main table in database function 
def collect_to_main_data_table_sqlite_database(animal_id, weight, scales_type):
    try:
        data_status = 'NO'
        last_drink_duration= 'NULL'
        data_collected_time = datetime.now()
        data_transfer_time = 'NULL'

        conn = sq3.connect('main_database.db')
        print("Opened database successfully")
        conn.execute("INSERT INTO COWS (CASE_ID, ANIMAL_ID, EVENT_TIME, WEIGHT, SCALES_TYPE, SPRAY_STATUS, SPRAY_TIME, DATA_STATUS, DATA_COLLECTED_TIME, DATA_TRANSFER_TIME ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                            (animal_id, event_time, weight, scales_type, last_drink_duration, data_status, data_collected_time, data_transfer_time))
        conn.commit()
        conn.close()

    except Exception as e:
        print("Error to save data in ", e)
    else:
        return 0

#################################################################################################
# Collect Raw data into raw data table by sqlite
def collect_to_raw_data_table_sqlite_database(animal_id, weight, scales_type):
    try:
        raw_data_status = 'NO'
        event_time = datetime.now()
        data_transfer_time = 'NULL'

        conn = sq3.connect('main_database.db')
        print("Opened database successfully")
        conn.execute("INSERT INTO RAW_DATA_TABLE (ANIMAL_ID, EVENT_TIME, WEIGHT, SCALES_TYPE, RAW_DATA_STATUS, DATA_TRANSFER_TIME ) VALUES(?, ?, ?, ?, ?, ?)",
                                            (animal_id, event_time, weight, scales_type, raw_data_status, data_transfer_time))
        conn.commit()
        conn.close()

    except Exception as e:
        print("Error to save data in ", e)
    else:
        return 0

#################################################################################################

def send_data_to_server_from_main_table(): # Sending data into Igor's server through JSON
    try:
        print("Extract data from database")

        # Extract info from cows table of main_database
        #    
        conn = sq3.connect('main_database.db')
        print("Opened database successfully")

        cursor = conn.execute("SELECT CASE_ID, ANIMAL_ID, EVENT_TIME, WEIGHT, SCALES_TYPE, LAST_DRINK_DURATION, MAIN_DATA_STATUS, DATA_TRANSFER_TIME from MAIN_DATA_TABLE")

        for row in cursor:
            if row[6] == 'NO': # check status in table
                #print("ANIMAL_ID = ", row[1])
                animal_id = row[1]
                #print("EVENT_TIME = ", row[2])
                event_time = row[2]
                #print("WEIGHT = ", row[3])
                weight = row[3]
                #print("SCALES_TYPE = ", row[4])
                scales_type = row[4]
                #print("DATA_STATUS = ", row[7])
                data_status = row[6]
                #case_id = 

                # Function of sending data from database to smart-farm server
                # def json_send_packet()
                
                #print("START SEND DATA TO SERVER:")
                url = 'http://194.4.56.86:8501/api/weights'
                headers = {'Content-type': 'application/json'}
                data = {"AnimalNumber" : animal_id,
                        "Date" : event_time,
                        "Weight" : weight,
                        "ScalesModel" : scales_type}
                answer = requests.post(url, data=json.dumps(data), headers=headers)
                print("Answer from server: ", answer) # Is it possible to stop on this line in the debug?
                print(answer.content)
                print(row[0])

                # Change status of DATA_STATUS in cows table from main_database 
                if 200 == answer.status_code:
                    #print("This is part of change status in cows table Data status")
                    # change status
                    data_for_query = ('YES', datetime.now() , row[0])
                    sqlite_querry = """UPDATE MAIN_DATA_TABLE SET MAIN_DATA_STATUS = ?, DATA_TRANSFER_TIME = ? WHERE CASE_ID = ?"""                 
                    conn.execute(sqlite_querry, data_for_query)
                    conn.commit()
          
                    
    except Exception as e:
        print("Error send data to server", e)
    else:
        print("Operation update database and sending to server done succesfully")
        conn.close()
        return 0
##########################################################################################


#def send_data_to_server_from_raw_table(): # Sending data into Igor's server through JSON



#######################################################################################

# internet connection check function
def check_internet_connection():
    """ Returns True if there's a connection """

    IP_ADDRESS_LIST = [
        "1.1.1.1",  # Cloudflare
        "1.0.0.1",
        "8.8.8.8",  # Google DNS
        "8.8.4.4",
        "208.67.222.222",  # Open DNS
        "208.67.220.220"
    ]

    port = 53
    timeout = 15

    for host in IP_ADDRESS_LIST:
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            pass
    else:
        print("No internet connection")
        return False 

#########################################################################################################################
# Send to raw data server directly from main function
def Send_RawData_to_server(animal_id, weight_new, type_scales): # Sending data into Igor's server through JSON
    try:
        print_log("START SEND RawDATA TO SERVER:")
        url = 'http://194.4.56.86:8501/api/RawWeights'
        headers = {'Content-type': 'application/json'}
        data = {"AnimalNumber" : animal_id,
                "Date" : str(datetime.now()),
                "Weight" : weight_new,
                "ScalesModel" : type_scales}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        print_log("Answer from RawData server: ", answer) # Is it possible to stop on this line in the debug?
        print_log("Content from RawData server: ", answer.content)
    except Exception as e:
        print_log("Error send data to RawData server", e)
    else:
        print_log("4 step send RawData")

def Connect_ARD_get_weight(cow_id, s, type_scales): # Connection to aruino through USB by Serial Port   
    try:
        print_log("CONNECT ARDUINO")
        s.flushInput() # Cleaning buffer of Serial Port
        s.flushOutput() # Cleaning output buffer of Serial Port
        print_log('Connect arduino after flush', s)
        print_log('Connect arduino s.name fuction answer :', s.name)
        print_log("Start collect weight")

        weight = (str(s.readline())) # Start of collecting weight data from Arduino
        print_log("First weight from Arduino", weight)
        print_log("After s.readline function")

        weight_new = re.sub("b|'|\r|\n", "", weight[:-5])

        print_log("Weight new after cleaning :", float(weight_new))
                
        weight_list = []
        #mid_weight = 0
        while (float(weight_new) > 10): # Collecting weight to array 
            weight = (str(s.readline()))
            weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
            print_log("Weight from Arduino :", weight_new)
            
            # Here the place to add RawWeights sending function
            #################################################################################
            Send_RawData_to_server(cow_id, weight_new, type_scales)
            # Change this functio to database select type 04/06/2022
            #################################################################################
            # End of Raw data function

            weight_list.append(float(weight_new))
        if weight_list == 0 or weight_list == []:
            return(-11)
        else:
            if weight_list != []: # Here must added check on weight array null value and one element array
                del weight_list[-1]
            
            # new method of averaging
            weight_finall = statistics.median(weight_list)
        
            #weight_finall = sum(weight_list) / len(weight_list) # Averaging weight array by sum and lenght
            #weight_finall = weight_finall/1000 # Dividing to 1000 for Igor's server  
            print_log("Weight_finall median :", "{0:.2f}".format(weight_finall))
            
            # Part of code to save all raw data into CSV file
            sep_line = "__________"
            # if cow_id != "b'0700010101001e4b'":            
            #     with open('raw_data.csv', 'a+', newline='') as csvfile:
            #         wtr = csv.writer(csvfile)
            #         wtr.writerow([sep_line])
            #         wtr.writerow([cow_id])
            #         wtr.writerow([datetime.now()])
            #         for x in weight_list : wtr.writerow ([x])
            #         print_log("Weight_list: ",weight_list)
            #     csvfile.close()
            ############################################################################
            # Check tomorrow how the collect data into sqlite  04/06/2022
            collect_to_raw_data_table_sqlite_database(animal_id=cow_id, weight=weight_finall, scales_type=type_scales)    
            ##############################################################################
            print_log("End of write raw data list :", weight_list)
            
            # End of collectin raw data into CSV file
            weight_list = []
            print_log("Weight_finall befor return :", weight_finall)
            return(float("{0:.2f}".format(weight_finall)))
    except Exception as e:
        print_log("Error connection to Arduino", e)
        return(-22)
    else:
        print_log("lid:Con_ARD: 1 step")
        print_log("lid:Con_ARD: 1 step")
        print_log("lid:Con_ARD: weight_finall in else", weight_finall)
        return(weight_finall)

def Connect_RFID_reader(): # Connection to RFID Reader through TCP and getting cow ID in str format
    try:    
        print_log("START RFID FUNCTION")
        ###########################################
        # TCP connection settings and socket
        TCP_IP = '192.168.1.250' #chafon 5300 reader address
        TCP_PORT = 60000 #chafon 5300 port
        BUFFER_SIZE = 1024
        animal_id = "b'435400040001'" # Id null starting variable
        animal_id_new = "b'435400040001'"
        #null_id = 435400040001 # Id null
        null_id = "b'435400040001'"
        print_log("START Animal ID animal_id: ", animal_id)
        print_log("START Null id null_id : ", null_id)
    
        if animal_id == null_id: # Send command to reader waiting id of animal
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(bytearray([0x53, 0x57, 0x00, 0x06, 0xff, 0x01, 0x00, 0x00, 0x00, 0x50])) #Chafon RU5300 Answer mode reading mode command
            data = s.recv(BUFFER_SIZE)
            animal_id= str(binascii.hexlify(data))
            animal_id_new = animal_id[:-4] #Cutting the string from unnecessary information after 4 signs 
            animal_id_new = animal_id_new[-12:] #Cutting the string from unnecessary information before 24 signs
            print_log("Raw ID animal_id: ", animal_id)
            print_log("New ID animal_id_new: ", animal_id_new)
            print_log("Null id null_id : ", str(null_id))
            s.close()             
        if animal_id_new == null_id: # Id null return(0)
            Connect_RFID_reader()
        else: # Id checkt return(1)
            animal_id = "b'435400040001'"
            print_log("Success step 2 RFID. animal id new:", animal_id_new)
            return(animal_id_new)
    except Exception as e:
        print_log("Error connect to Arduino ", e)
    else: 
        print_log("2 step RFID")
    
def Send_data_to_server(animal_id, weight_finall, type_scales): # Sending data into Igor's server through JSON
    try:
        print_log("START SEND DATA TO SERVER:")
        url = 'http://194.4.56.86:8501/api/weights'
        headers = {'Content-type': 'application/json'}
        data = {"AnimalNumber" : animal_id,
                "Date" : str(datetime.now()),
                "Weight" : weight_finall,
                "ScalesModel" : type_scales}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        print_log("Answer from server: ", answer) # Is it possible to stop on this line in the debug?
        print_log("Content from main server: ", answer.content)
    except Exception as e:
        print_log("Error send data to server", e)
    else:
        print_log("4 step send data")

def Collect_data_CSV(cow_id, weight_finall, type_scales): # Collocting datat into CSV, in the future must be in SQLite
    try:
        print_log("START COLLECT DATA TO CSV")
        date_now = (str(datetime.now()))
        row = [cow_id, weight_finall,  date_now, type_scales]
    
        with open('cows_database.csv', 'a', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(row)
        writeFile.close()
    except Exception as e:
        print_log("Error to write file")
    else:
        print_log("3 step collect data")   


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
