
#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    print(f'start dist func')
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    print(1)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    print(2)
    StartTime = time.time()
    StopTime = time.time()
    print(3)
    # save StartTime
    print(GPIO.input(GPIO_ECHO)) 
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        print(f'StartTime', StartTime)
        print(f'Start GPIO_ECHO')
        print(GPIO.input(GPIO_ECHO))
    print(4)
    print(f'After Start GPIO_ECHO')
    print(GPIO.input(GPIO_ECHO))
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        print(f'StopTime', StopTime)
        print(f'Stop GPIO_ECHO')
        print(GPIO.input(GPIO_ECHO))
    print(5)
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
