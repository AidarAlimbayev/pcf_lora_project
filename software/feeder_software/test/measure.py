#!/usr/bin/sudo python3
import software.feeder_software.test._headers as hdr

requirement_list = ['loguru', 'requests', 'numpy', 'RPi.GPIO']
hdr.install_packages(requirement_list)

import RPi.GPIO as GPIO
from loguru import logger
from software.feeder_software.test._hx7 import HX711
import time
import sys
import software.feeder_software.test._config as cfg


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
        item_weight = input("Please enter the item's weight in kg.\n>")
        scale = int(measured_weight)/int(item_weight)
        hx.set_scale(scale)
        logger.info("Scale adjusted for kilograms: {}".format(scale))
        logger.info(f'Offset: {offset}, set_scale(scale): {scale}')
        GPIO.cleanup()
        cfg.update_setting("Calibration", "Offset", offset)
        cfg.update_setting("Calibration", "Scale", scale)
        return offset, scale
    except:
        logger.error(f'calibrate Fail')


def measure():
    try:
        GPIO.setmode(GPIO.BCM)  
        hx = HX711(21, 20, gain=128)
        offset = float(cfg.get_setting("Calibration" "Offset"))
        scale = float(cfg.get_setting("Calibration", "Scale"))
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
            print("Hi! It is measure test file.\n For first you should to make a choice:")
            print("1. Make calibration\n 2. Start measure.")
            print("If you use this sketch first time please make calibration\n to save needed values.\n")
            #print("Please don't forget change offset and scale value in measure function!!!")
            choice = input()
            if choice == 1:
                calibrate()
            while True:
                print(measure())
    except ValueError as v:
        print(v)

main()