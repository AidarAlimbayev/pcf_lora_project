import serial

#serial_port = '/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'
#serial_port = '/dev/serial/by-path/pci-0000:00:14.0-usb-0:1:1.0-port0'
serial_port = '/dev/ttyUSB0'

baud_rate = 57600

ser = serial.Serial(serial_port, baud_rate)

# Open the serial port
ser = serial.Serial(serial_port, baud_rate)

try:
    # Send data
    ser.write(b'Hello, world!')

    #read data = 0x02
    #example of bytearray([0x53, 0x57, 0x00, 0x25, 0xFF, 0x21, 0xC3, 0x55, 0x02, 0x01, 0x00, 0x00, 0x1A, 0x01, 0x04, 0x4E, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x1E, 0x0A, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x51]))    
    bytearray([0x04, 0xff, 0x01, 0x00, 0x14, 0x14, 0x14, 0x14])    

    

    #hex_command = bytearray([0x04, 0xff, 0x01, 0x00, 0x14, 0x14, 0x14, 0x14])   
    hex_command = '04ff010014141414'


    print("Hex command from bytearray: ", hex_command)
    command_bytes = bytes.fromhex(hex_command)
    print("Hex command command bytes: ", command_bytes)
    ser.write(command_bytes)

    # Read data
    received_data = ser.readline()
    print("Received data: ", received_data.decode('utf-8'))

finally:
    # Close the serial port, even if an exception occurs
    ser.close()


# CRC16 checksum calculations in python
#import crcmod

# def calculate_crc16(data):
#     crc16_func = crcmod.mkCrcFun(0x18005, initCrc=0, rev=True)  # CRC-16-CCITT
#     crc16_checksum = crc16_func(data)
#     return crc16_checksum

# # Example usage:
# data = b"Hello, world!"
# crc16_result = calculate_crc16(data)

# print(f"CRC16 checksum for '{data.decode()}' is: {crc16_result}")



# try:
#     # Send a hex command (e.g., 0x01, 0xA2, 0xFF)
#     # 0x02
 
#     #hex_command = '02'
#     #command_bytes = bytes.fromhex(hex_command)
#     #ser.write(command_bytes)

#     # Read response
#     response = ser.readline()
#     print("Received response: ", response.decode('utf-8'))

# finally:
#     # Close the serial port, even if an exception occurs
#     ser.close()



# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((UART, TCP_PORT))
# #s.send(bytearray([0x06, 0x00, 0x01, 0x04, 0xff, 0xd4, 0x39])) # Chafon RU6403 reading command
# #s.send(bytearray([0x53, 0x57, 0x00, 0x03, 0xff, 0xe0, 0x74])) #Chafon RU5300 Active mode reading mode command
# s.send(bytearray([0x53, 0x57, 0x00, 0x06, 0xff, 0x01, 0x00, 0x00, 0x00, 0x50])) #Chafon RU5300 Answer mode reading mode command
# data = s.recv(BUFFER_SIZE)
# animal_id= str(binascii.hexlify(data))
#         #print("Received ID cow: ")
# #print(animal_id)

# animal_id_new = animal_id[:-5] #Cutting the string from unnecessary information after 7 signs 
# animal_id_new = animal_id_new[-12:] #Cutting the string from unnecessary information before 24 signs

# print("CUT new ID cow: ")
# print(animal_id_new)