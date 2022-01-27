import RPi.GPIO as GPIO
import time

# Module level constants
LED1 = 14
LED2 = 7

# Sets up pins as outputs
def setup(*leds):
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    for led in leds:
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, GPIO.LOW)

# Turn on and off the leds
def blink(*leds):
    # Blink all leds passed
    for led in leds:
        GPIO.output(led, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(led, GPIO.LOW)

if __name__ == '__main__':
    # Setup leds
    setup(LED1, LED2)
    # Run blinking forever
    try:
        while True:
            blink(LED1, LED2)
    # Stop on Ctrl+C and clean up
    except KeyboardInterrupt:
        GPIO.cleanup()