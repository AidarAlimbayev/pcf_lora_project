import serial
from time import sleep

uart_serial = serial.Serial("/dev/ttyS0", 9600, timeout = 3.0)

trans_word = "Hello\r\n"
print(trans_word)
uart_serial.write("Help01".encode())
print("Hello01\r\n".encode())
uart_serial.write("123\r\n".encode())
print(uart_serial.close())

print("Sanat Jopa")



