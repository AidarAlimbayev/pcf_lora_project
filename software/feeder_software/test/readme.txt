feeder_test readme...

path of test files software/feeder_software/test

Here you have 5 python files. Actually, for test you can use just two files:

1. measure.py - calibration and make a measure of weight
2. ultrasonic.py - for take a value from ultrasonic device.

For ultrasonic use this gpio pins:

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24

Do not forget about BCM board. https://toptechboy.com/understanding-raspberry-pi-4-gpio-pinouts/

