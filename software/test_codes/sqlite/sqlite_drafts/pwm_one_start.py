#import lib_pcf_ver45 as pcf
import RPi.GPIO as GPIO
import time

# variable by default power = 100
# variable by default duration = 10

print("Start PWM function")

#power = float(input("Enter power: "))
duration = float(input("Enter duration: "))
#pcf.PWM_GPIO_RASP(power, duration)
pin = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)
GPIO.setup(pin,GPIO.OUT)
GPIO.output(pin,GPIO.HIGH)

time.sleep(duration)

GPIO.output(pin,GPIO.LOW)

GPIO.cleanup()

print("End PWM function")