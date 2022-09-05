from datetime import datetime
from loguru import logger
import RPi.GPIO as GPIO
import time
import re
import binascii
import socket


def distance():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO_TRIGGER = 18
        GPIO_ECHO = 24
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        GPIO.output(GPIO_TRIGGER, True)                 # set Trigger to HIGH
        time.sleep(0.00001)                             # set Trigger after 0.01ms to LOW
        GPIO.output(GPIO_TRIGGER, False)
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(GPIO_ECHO) == 0:               # save StartTime
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()                      # save time of arrival
        TimeElapsed = StopTime - StartTime              # time difference between start and arrival
        """multiply with the sonic speed (34300 cm/s)
        and divide by 2, because there and back"""
        distance = (TimeElapsed * 34300) / 2
        return distance
    except:
        logger.error(f'Distance func error')
 
def measuring_start(distance):
    try:
        if distance <= 50:
            return True
        else:
            return False
    except ValueError as v:
        logger.error(f'Measurement stopped {v}')

def post_request(feeder_type, serial_number, feed_time, animal_id, end_weight, feed_weight):
    try:
        payload = {
            "Eventdatetime": str(datetime.now()),
            "EquipmentType": feeder_type,
            "SerialNumber": serial_number,
            "FeedingTime": feed_time,
            "RFIDNumber": animal_id,
            "WeightLambda": end_weight,
            "FeedWeight": feed_weight
        }
        return payload
    except ValueError as v:
        logger.error(f'Post_request function error: {v}')

def Connect_RFID_reader():                                      # Connection to RFID Reader through TCP and getting cow ID in str format
    try:    
        logger.debug(f'START RFID FUNCTION')
        TCP_IP = '192.168.1.250'                                #chafon 5300 reader address
        TCP_PORT = 60000                                        #chafon 5300 port
        BUFFER_SIZE = 1024
        animal_id = "b'435400040001'"                           # Id null starting variable
        animal_id_new = "b'435400040001'"
        null_id = "b'435400040001'"
        logger.debug(f'START Animal ID animal_id: {animal_id}')
        logger.debug(f'START Null id null_id : {null_id}')
    
        if animal_id == null_id: # Send command to reader waiting id of animal
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(bytearray([0x53, 0x57, 0x00, 0x06, 0xff, 0x01, 0x00, 0x00, 0x00, 0x50])) #Chafon RU5300 Answer mode reading mode command
            data = s.recv(BUFFER_SIZE)
            animal_id= str(binascii.hexlify(data))
            animal_id_new = animal_id[:-5] #Cutting the string from unnecessary information after 4 signs 
            animal_id_new = animal_id_new[-12:] #Cutting the string from unnecessary information before 24 signs
            logger.debug(f'Raw ID animal_id: {animal_id}')
            logger.debug(f'New ID animal_id_new: {animal_id_new}')
            logger.debug(f'Null id null_id : {str(null_id)}')
            s.close()             
        if animal_id_new == null_id: # Id null return(0)
            Connect_RFID_reader()
        else: # Id checkt return(1)
            animal_id = "b'435400040001'"
            logger.debug(f'Success step 2 RFID. animal id new: {animal_id_new}')
            return(animal_id_new)
    except Exception as e:
        logger.error(f'Error connect to Arduino {e}')
    else: 
        logger.debug(f'2 step RFID')

def rfid_label():
    try:
        labels = []
        while len(labels) <= 11:
            cow_id = Connect_RFID_reader()
            labels.append(cow_id)
        animal_id = max([j for i,j in enumerate(labels) if j in labels[i+1:]]) if labels != list(set(labels)) else -1
        return animal_id
    except ValueError as v:
        logger.error(f'Post_request function error: {v}')

def instant_weight(s):
    try:
        s.flushInput() 
        weight = (str(s.readline())) 
        weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
        return weight_new
    except ValueError as e:
        logger.error(f'Instant_weight function Error: {e}')


