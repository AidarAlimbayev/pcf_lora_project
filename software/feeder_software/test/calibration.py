import RPi.GPIO as GPIO
from loguru import logger
from hx7 import HX711


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
        #cfg.update_setting("Calibration", "Offset", offset)
        #cfg.update_setting("Calibration", "Scale", scale)
        return offset, scale
    except:
        logger.error(f'calibrate Fail')

