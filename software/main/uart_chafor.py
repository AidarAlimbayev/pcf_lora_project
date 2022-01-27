#uart_chafor.py

import serial

ser = serial.Serial('/dev/ttyUSB0')
print(ser.name)
string = "\x53\x57\x00\x03\xFF\x20\x34"
ser.write(hex(string))

# Data send to 
# 53 57 00 03 FF 20 34

ser.close()