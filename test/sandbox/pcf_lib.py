#pcf_lib.py
from datetime import datetime, date, time
import time
import csv
import logging
import logging.config


type_scales = "Scale_A"

def logging_start():
    logging.config.fileConfig('logging.config')
    logger = logging.getLogger("pcf_sandbox")
    logger.info("Program started")


#connect_id.py
def connect_id():
    logging.config.fileConfig('logging.config')
    logger = logging.getLogger("pcf_connect_id")
    print("Try to connect RFID")
    logger.info("Start to connect RFID")
    cow_id = str(input("Enter ID: "))
    if cow_id == 0:
        quit()
    else:
        logger.info("Entered ID: %s", cow_id)
        return(float(cow_id))

#collect_data.py
def collect_data(cow_id, weight_finall):
    logging.config.fileConfig('logging.config')
    logger = logging.getLogger("pcf_collect_data")
    logger.info("Start tot collect data to csv file")
    date_now = (str(datetime.now()))
    row = [cow_id, weight_finall,  date_now, type_scales]
    with open('test_algorithm.csv', 'a', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(row)
    logger.info("Data written to test_algorithm.csv!")
    writeFile.close()
    weight_finall = 0 

#connect_weight.py
def connect_weight():
    logging.config.fileConfig('logging.config')
    logger = logging.getLogger("pcf_connect_weight")
    weight_list = []
    print("Measure weight of cow")
    logger.info("Measure weight of cow")
    weight = float(input("Enter weight: "))
    logger.info("Entered weight is: %f", weight)
    while (float(weight) != 0):
        weight = float(input("Enter weight:___"))
        logger.info("Entered weight is: %f", weight)
        weight_list.append(float(weight))
    if weight_list == 0 or weight_list == []:
        return(0)
    else:
        if weight_list != 0:
            print ("Weight list: ", weight_list)
            logger.info("Weight list is:", weight_list)
            del weight_list[-1]

        weight_finall =  sum(weight_list) / len(weight_list) 
        weight_list = []
        logger.info("Weight finall is: %f", weight_finall)
        return(float(weight_finall))

#send_server.py


def send_server(cow_id, weight_finall):
    logging.config.fileConfig('logging.config')
    logger = logging.getLogger("pcf_send_server")
    logger.info("Start to send data to server")
    print("ID:", cow_id)
    logger.info("ID: %s", cow_id)
    print("Weight:", weight_finall)
    logger.info("ID: %f", weight_finall)
    print("Date:", str(datetime.now()))
    logger.info("Date: %s", str(datetime.now()))
    print ("Scale type:", type_scales)
    logger.info("Scale type: %s", type_scales)