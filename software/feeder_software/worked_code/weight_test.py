import lib_feeder as fdr
import RPi.GPIO as GPIO
from hx711 import HX711

calibrated_ratio = 3.1026918536009447

GPIO.setmode(GPIO.BCM)  
hx = HX711(dout_pin=21, pd_sck_pin=20)
hx.set_scale_ratio(calibrated_ratio)
err = hx.zero()
    # check if successful
if err:
    raise ValueError('Tare is unsuccessful.')

#GPIO.cleanup()

def weight_test():
    try:
        while True:
            print(fdr.raspberry_weight(hx))
        
    except ValueError as e:
        print("Error ", e)

weight_test()