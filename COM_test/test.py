import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=15)


print(ser.name)

ser.write("04ff211995")
print(ser.read())
ser.close()