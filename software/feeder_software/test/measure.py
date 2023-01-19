import RPi.GPIO as GPIO
from loguru import logger
from hx7 import HX711
import time
import calibration as cal
import sys

def measure():
    try:
        GPIO.setmode(GPIO.BCM)  
        hx = HX711(21, 20, gain=128)
        offset = 0 # Put here calibration offset value
        scale = 0 # Put here calibration scale value
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


def cleanAndExit():
    logger.info("Cleaning up...")
    GPIO.cleanup()
    logger.info("Bye!")
    sys.exit()


def main():
    try: 
        while True:
            print("Hi is it measure test file.\n For first you should to make a choice:")
            print("1. Make calibration\n 2. Start measure.")
            print("Please don't forget change offset and scale value in measure function!!!")
            choice = input()
            if choice == 1:
                cal.calibrate()
            else:
                measure()
    except ValueError as v:
        print(v)

main()