import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

switch = 4

GPIO.setup(switch, GPIO.IN, GPIO.PUD_UP)

while True:
    switch_state = GPIO.input(switch)
    if switch_state == GPIO.HIGH:
      print ("HIGH")
    else:
      print ("LOW")
    time.sleep(0.5)