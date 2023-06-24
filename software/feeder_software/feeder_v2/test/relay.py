import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIN_NUMBER = 17
GPIO.setup(PIN_NUMBER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    relay_state = GPIO.input(PIN_NUMBER)

    if relay_state == GPIO.HIGH:
        print("Реле замкнуто")
    else:
        print("Реле разомкнуто")

#    time.sleep(0.5)


