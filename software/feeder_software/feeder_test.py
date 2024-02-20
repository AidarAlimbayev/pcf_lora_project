from datetime import datetime
from loguru import logger
import RPi.GPIO as GPIO
import time
import re
import binascii
import socket
import sys
from hx7 import HX711
import numpy

<<<<<<< HEAD
=======
calibrated_ratio = 256757

def hx711_calibrate(hx):
    try:            
        GPIO.setmode(GPIO.BCM)
        hx = HX711(dout_pin=21, pd_sck_pin=20)
        err = hx.zero()
        # check if successful
        if err:
            raise ValueError(logger.error(f'Tare is unsuccessful.'))

        reading = hx.get_raw_data_mean()
        if reading:  # always check if you get correct value or only False
            # now the value is close to 0
            logger.info(f'Data subtracted by offset but still not converted to units: {reading}')
        else:
            logger.info(f'invalid data {reading}')

        input(f'Put known weight on the scale and then press Enter')
        reading = hx.get_data_mean()
        if reading:
            logger.info(f'Mean value from HX711 subtracted by offset: {reading}')
            known_weight_grams = input(
                f'Write how many grams it was and press Enter: ')
            try:
                value = float(known_weight_grams)
                logger.info(value, 'grams')
            except ValueError:
                logger.info('Expected integer or float and I have got:',
                    known_weight_grams)

            # set scale ratio for particular channel and gain which is
            # used to calculate the conversion to units. Required argument is only
            # scale ratio. Without arguments 'channel' and 'gain_A' it sets
            # the ratio for current channel and gain.
            ratio = reading / value  # calculate the ratio for channel A and gain 128
            hx.set_scale_ratio(ratio)  # set ratio for current channel
            logger.info(f'Ratio is: {ratio}')
        else:
            raise ValueError(logger.error(f'Cannot calculate mean value. Try debug mode. Variable reading: {reading}'))
          
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bye :)')

    finally:
        GPIO.cleanup()
        return ratio
        
def raspberry_weight(calibrated_ratio):
    try:
        GPIO.setmode(GPIO.BCM)  
        hx = HX711(dout_pin=21, pd_sck_pin=20)
        hx.set_scale_ratio(calibrated_ratio)
        weight_kg = hx.get_weight_mean(10)/1000
    except:
        logger.error(f'raspberry weight func error: {b}')
    finally:
        GPIO.cleanup()
        return weight_kg
>>>>>>> 8da6cf3 (weight test)

def distance():
    try:
        dist_list = []
        while len(dist_list) < 10:
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
            dist_list.append(distance)
            GPIO.cleanup()
        total = numpy.mean(dist_list)
        #total = max([j for i,j in enumerate(dist_list) if j in dist_list[i+1:]]) if dist_list != list(set(dist_list)) else -1
        return round(total, 2)
    except TypeError as t:
        logger.error(f'Distance func error {t}')


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
        #logger.debug(f'START RFID FUNCTION')
        TCP_IP = '192.168.1.250'                                #chafon 5300 reader address
        TCP_PORT = 60000                                        #chafon 5300 port
        BUFFER_SIZE = 1024
        animal_id = "b'435400040001'"                           # Id null starting variable
        animal_id_new = "b'435400040001'"
        null_id = "b'435400040001'"
        #logger.debug(f'START Animal ID animal_id: {animal_id}')
        #logger.debug(f'START Null id null_id : {null_id}')
    
        if animal_id == null_id: # Send command to reader waiting id of animal
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(bytearray([0x53, 0x57, 0x00, 0x06, 0xff, 0x01, 0x00, 0x00, 0x00, 0x50])) #Chafon RU5300 Answer mode reading mode command
            data = s.recv(BUFFER_SIZE)
            animal_id= str(binascii.hexlify(data))
            animal_id_new = animal_id[:-5] #Cutting the string from unnecessary information after 4 signs 
            animal_id_new = animal_id_new[-12:] #Cutting the string from unnecessary information before 24 signs
           # logger.debug(f'Raw ID animal_id: {animal_id}')
            #logger.debug(f'New ID animal_id_new: {animal_id_new}')
            #logger.debug(f'Null id null_id : {str(null_id)}')
            s.close()             
        if animal_id_new == null_id: # Id null return(0)
            Connect_RFID_reader()
        else: # Id checkt return(1)
            animal_id = "b'435400040001'"
            #logger.debug(f'Success step 2 RFID. animal id new: {animal_id_new}')
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


# def instant_weight(s):
#     try:
#         s.flushInput() 
#         weight = (str(s.readline())) 
#         weight_new = re.sub("b|'|\r|\n", "", weight[:-5])
#         return weight_new
#     except ValueError as e:
#         logger.error(f'Instant_weight function Error: {e}')


def calibrate():
    try:
        GPIO.setmode(GPIO.BCM)  
        logger.info('Start calibrate function')
        hx = HX711(21, 20, gain=128)
        readyCheck = input("Remove any items from scale. Press any key when ready.")
        offset = hx.read_average()
        logger.info("Value at zero (offset): {}".format(offset))
        hx.set_offset(offset)
        logger.info("Please place an item of known weight on the scale.")
        readyCheck = input("Press any key to continue when ready.")
        measured_weight = (hx.read_average()-hx.get_offset())
        item_weight = input("Please enter the item's weight in grams.\n>")
        scale = int(measured_weight)/int(item_weight)
        hx.set_scale(scale)
        logger.info("Scale adjusted for grams: {}".format(scale))
        logger.info(f'Offset: {offset}, set_scale(scale): {scale}')
        GPIO.cleanup()
        return offset, scale
    except:
        logger.error(f'calibrate Fail')


def cleanAndExit():
    logger.info("Cleaning up...")
    GPIO.cleanup()
    logger.info("Bye!")
    sys.exit()

def measure(offset, scale):
    try:
        GPIO.setmode(GPIO.BCM)  
        hx = HX711(21, 20, gain=128)
        hx.set_scale(scale)
        hx.set_offset(offset)
        val = hx.get_grams()
        hx.power_down()
        time.sleep(.001)
        hx.power_up()
        GPIO.cleanup()
        return round(val,2)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()