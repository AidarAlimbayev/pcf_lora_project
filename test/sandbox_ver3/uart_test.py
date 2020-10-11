import serial
import time
import datetime
from time import sleep
from datetime import date

#uart_serial = serial.Serial("/dev/ttyS0", 9600, timeout = 3.0)

trans_word = "Hello\r\n"
print(trans_word)
#uart_serial.write("Help01".encode())
print("Hello01\r\n".encode())
#uart_serial.write("123\r\n".encode())
#print(uart_serial.close())

print("----------------------")
print("Start sending to Lora!")
#02340490e462,79.053,2020-06-06 20:07:52.810774,Scale_A #typical cow data in csv

animal_id = "02340490e462"
weight_finall = 129.5
types_scales = "akkol-1"

#print(len(animal_id.encode('utf-8')))
hex_id = bytearray.fromhex(animal_id)
print(hex_id)
#print(str.encode(hex_id))


#dt = datetime.fromtimestamp(timestamp)
time_now = int(time.time())
#print(time_now)

#print(len(weight_finall.encode('utf-8')))
split_num = str(weight_finall).split('.')
int_part = int(split_num[0])
decimal_part = int(split_num[1])
print(int_part.to_bytes(2, 'little'))
print("----------------------------")
print(decimal_part.to_bytes(1, 'little'))

#print(type(decimal_part.to_bytes(1, 'little')))


#print(len(types_scales.encode('utf-8')))
        # data = {"AnimalNumber" : animal_id,
        #         "Date" : str(datetime.now()),
        #         "Weight" : weight_finall,
        #         "ScalesModel" : type_scales}

