import time
import smtplib
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, GPIO.PUD_DOWN)

GPIO_PWM_0 = 13
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_PWM_0, GPIO.OUT)

pi_pwm = GPIO.PWM(GPIO_PWM_0, 100)

while True:
    if GPIO.input(23):
        pi_pwm.start(0)
        pi_pwm.ChangeDutyCycle(50)
    else:
        pi_pwm.ChangeDutyCycle(0)
        pi_pwm.stop()
