import serial 
from time import sleep

uart_serial = serial.Serial("/dev/ttyS0", 9600, timeout = 3.0)

trans_word = "Hello\r\n"
print(trans_word)
uart_serial.write(trans_word.encode())
uart_serial.close()

print("end of transmit")