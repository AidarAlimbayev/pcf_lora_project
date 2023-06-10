
import lib_test as pcf
import time
#time.sleep(10)
from datetime import datetime, time
from loguru import logger
import _config as cfg
import time
import adc_data as ADC


@logger.catch
def main():
        port = cfg.get_setting("Parameters", "arduino_port")
        arduino = ADC.ArduinoSerial(port)
        arduino.connect()
        offset, scale = float(cfg.get_setting("Calibration", "offset")), float(cfg.get_setting("Calibration", "scale"))
        arduino.set_offset(offset)
        arduino.set_scale(scale)
   
        while(True):
            try:
                print(arduino.get_measure())
                time.sleep(1)
            except KeyboardInterrupt as k:
                arduino.disconnect()
                

main()