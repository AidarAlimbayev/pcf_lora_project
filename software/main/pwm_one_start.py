import lib_pcf_ver4 as pcf

# variable by default power = 100
# variable by default duration = 10

print("Start PWM function")

power = float(input("Enter power: "))
duration = float(input("Enter duration: "))

pcf.PWM_GPIO_RASP(power, duration)

print("End PWM function")