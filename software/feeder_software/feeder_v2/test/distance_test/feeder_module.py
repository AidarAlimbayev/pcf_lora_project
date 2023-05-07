"""Feeder version 3. Edition by Suieubayev Maxat.
feeder_module.py - это модуль функции кормушки. 
Contact number +7 775 818 48 43. Email maxat.suieubayev@gmail.com"""

#!/usr/bin/sudo python3

from loguru import logger
import re
import time

def connect_arduino_to_get_dist(s):
    # s.flushInput() # Cleaning buffer of Serial Port
    # s.flushOutput() # Cleaning output buffer of Serial Port
    # time.sleep(0.001)
    # distance = (str(s.readline()))
    # distance = re.sub("b|'|\r|\n", "", distance[:-5])
    distance = s.readline().decode().strip() 
    #while (float(distance)) < 50:
    #    distance = (str(s.readline()))
    #    distance = re.sub("b|'|\r|\n", "", distance[:-5])
    #    distance = float(distance)
    #    return distance
    return distance

