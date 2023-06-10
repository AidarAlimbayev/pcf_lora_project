#!/usr/bin/python3

import RPi.GPIO as GPIO
import time



GPIO.setmode(GPIO.BCM)  # Устанавливаем BCM-нумерацию пинов
GPIO.setup(18, GPIO.OUT)  # Устанавливаем 18-й пин как выход
GPIO.output(18, GPIO.LOW)
GPIO.setup(23, GPIO.OUT)  # Устанавливаем 18-й пин как выход
GPIO.output(23, GPIO.LOW)
def main():
    try:
        print("Enter On time: ")
        on_time = input()
        print("Enter off time: ")
        off_time = input()
        count = 0
        while(True):
            print("On")
            GPIO.output(18, GPIO.HIGH)  # Подаём 3.3 вольта на 18-й пин
            GPIO.output(23, GPIO.HIGH)
            time.sleep(float(on_time))  # Ждём одну секунду
            count += 1
            print("off")
            GPIO.output(18, GPIO.LOW)  # Подаём 3.3 вольта на 18-й пин
            GPIO.output(23, GPIO.LOW)
            time.sleep(float(off_time))
    except KeyboardInterrupt as e:
        print("Ok! Bye!")
        print("Count of cycles: ", count)
        GPIO.cleanup()  # Возвращаем пины в исходное состояние

main()
