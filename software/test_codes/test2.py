import threading
import queue
import time

while(True):
    distance = int(input("Please enter value: "))
    if distance < 60 or distance > 120:
        print("False")
    else:
        print("True")