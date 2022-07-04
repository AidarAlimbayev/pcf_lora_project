#import RPi.GPIO as GPIO
import time
from urllib import response
import requests

try: 
    url = 'url'
    request = requests.get(url)
    response = request.json()
    timer = response['timer']
    Cow_ID = response['Cow_Id']

