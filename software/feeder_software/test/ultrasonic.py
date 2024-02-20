#!/usr/bin/sudo python3
import software.feeder_software.test._headers as hdr

requirement_list = ['loguru', 'requests', 'numpy', 'RPi.GPIO']
hdr.install_packages(requirement_list)

import RPi.GPIO as GPIO
import time
import numpy
from loguru import logger
import re

#def distance():
 #   try:
     #   dist_list = []
     #   while len(dist_list) < 10:
      #      GPIO.setmode(GPIO.BCM)
      #      GPIO_TRIGGER = 18
      #      GPIO_ECHO = 24
       #     GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
       #     GPIO.setup(GPIO_ECHO, GPIO.IN)
       #     GPIO.output(GPIO_TRIGGER, True)                 # set Trigger to HIGH
        #    time.sleep(0.00001)                             # set Trigger after 0.01ms to LOW
        #    GPIO.output(GPIO_TRIGGER, False)
        #    StartTime = time.time()
        #    StopTime = time.time()
         #   while GPIO.input(GPIO_ECHO) == 0:               # save StartTime
         #       StartTime = time.time()
         #   while GPIO.input(GPIO_ECHO) == 1:
          #      StopTime = time.time()                      # save time of arrival
          #  TimeElapsed = StopTime - StartTime              # time difference between start and arrival
          #  """multiply with the sonic speed (34300 cm/s)
          #  and divide by 2, because there and back"""
          #  distance = (TimeElapsed * 34300) / 2
          #  dist_list.append(distance)
          #  GPIO.cleanup()
        #total = numpy.mean(dist_list)
        #total = max([j for i,j in enumerate(dist_list) if j in dist_list[i+1:]]) if dist_list != list(set(dist_list)) else -1
       # return round(total, 2)
    #except TypeError as t:
    #    logger.error(f'Distance func error {t}')


def connect_arduino_to_get_dist(s):
    distance = (str(s.readline()))
    distance = re.sub("b|'|\r|\n", "", distance[:-5])
    while (float(distance)) < 150:
        distance = (str(s.readline()))
        distance = re.sub("b|'|\r|\n", "", distance[:-5])
        return distance
    return distance

    
def main():
    while True:
        distance = distance()
        print(distance)

main()