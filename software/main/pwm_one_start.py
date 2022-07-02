import lib_pcf_ver4 as pcf
import RPi.GPIO as GPIO

# variable by default power = 100
# variable by default duration = 10

print("Start PWM function")

#power = float(input("Enter power: "))
duration = float(input("Enter duration: "))

#pcf.PWM_GPIO_RASP(power, duration)

print("Start PWM function to spray command from raspberry")
        #GPIO_PWM_0 = 32                
pin = 40 # 5,7,10 scales on 40 pin ## 6 scales on 33 pin, 
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40,GPIO.HIGH)
pcf.time.sleep(duration)
GPIO.output(40, GPIO.LOW)
GPIO.cleanup()

print("End PWM function")