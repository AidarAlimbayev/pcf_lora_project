from datetime import datetime, date, time
import time
import socket
import binascii
import csv
import re

def choose_power():
    set_power = input("Choose antenna power in range [1, 3, 5, 7, 10, 15, 20, 26] :")
        #print(type(set_power))
    if set_power == '1':
        print("Power of antenna = 1 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x01, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x6A]))
    if set_power == '3':
        print("Power of antenna = 3 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x03, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x68]))
    if set_power == '5':
        print("Power of antenna = 5 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x05, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x66]))
    if set_power == '7':
        print("Power of antenna = 7 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x07, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64]))
    if set_power == '10':
        print("Power of antenna = 10 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x0A, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x61]))
    if set_power == '15':
        print("Power of antenna = 15 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x0F, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5C]))

    if set_power == '19':
        print("Power of antenna = 26 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x16, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x51]))     


    if set_power == '20':
        print("Power of antenna = 20 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x14, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x57]))

    if set_power == '21':
        print("Power of antenna = 26 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x15, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x51]))     

    if set_power == '22':
        print("Power of antenna = 26 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x16, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x51]))     

    if set_power == '23':
        print("Power of antenna = 26 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x17, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x51]))     

    if set_power == '24':
        print("Power of antenna = 26 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x18, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x51]))     
 
    if set_power == '25':
        print("Power of antenna = 26 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x19, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x51]))     
    if set_power == '26':
        print("Power of antenna = 26 dbm")
        return(bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x1A, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x51]))    
    else:
        print("Please choose number from range!")
        choose_power()

def set_power_RFID():
    ###########################################
    # TCP connection settings and socket
    TCP_IP = '192.168.1.250' #chafon 5300 reader address
    TCP_PORT = 60000 #chafon 5300 port
    BUFFER_SIZE = 1024

    #animal_id = "b'0700010101001e4b'" # Id null starting variable
    #null_id = "b'0700010101001e4b'" # Id null

    print("Start configure antenna power")
    #if animal_id == null_id: # Send command to reader waiting id of animal
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(choose_power()) #
    data = s.recv(BUFFER_SIZE)
    #print(data)

    recieved_data = str(binascii.hexlify(data))
    #print("binary expectation of data")
    #print(recieved_data)
    check_code = "b'4354000400210143'"
    #print(check_code)
    if recieved_data == check_code:
        print("operation succeeded")
    else: 
        print("Denied!")
    s.close()              

set_power_RFID()

# 1 dBm, Eur, RJ45, 115200,  ActMode
# (0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x01, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x6A)

# 3 dBm, Eur, RJ45, 115200,  ActMode
# (0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x03, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x68)

# 5 dBm, Eur, RJ45, 115200,  ActMode
# (0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x05, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x66)

# 7 dBm, Eur, RJ45, 115200,  ActMode
# (0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x07, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x64)

# 15 dBm, Eur, RJ45, 115200, ActMode
# (0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x0F, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5C)

# 20 dBm, Eur, RJ45, 115200, ActMode
# (0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x14, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x57)

# 26 dBm, Eur, RJ45, 115200, ActMode
# (0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x1A, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x51)

# recieved message Operation succeeded
# (0x43, 0x54, 0x00, 0x04, 0x00, 0x21, 0x01, 0x43)
