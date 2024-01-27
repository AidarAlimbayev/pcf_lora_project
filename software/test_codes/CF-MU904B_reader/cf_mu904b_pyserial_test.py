import serial

#serial_port = '/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'
serial_port = '/dev/serial/by-path/pci-0000:00:14.0-usb-0:1:1.0-port0'

baud_rate = 57600

# # Open the serial port
# ser = serial.Serial(serial_port, baud_rate)

# try:
#     # Send data
#     ser.write(b'Hello, world!')

#     # Read data
#     received_data = ser.readline()
#     print("Received data: ", received_data.decode('utf-8'))

# finally:
#     # Close the serial port, even if an exception occurs
#     ser.close()


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

ser = serial.Serial(serial_port, baud_rate)

try:
    # Send a hex command (e.g., 0x01, 0xA2, 0xFF)
    # 0x02
 
    #hex_command = '02'
    #command_bytes = bytes.fromhex(hex_command)
    #ser.write(command_bytes)

    # Read response
    response = ser.readline()
    print("Received response: ", response.decode('utf-8'))

finally:
    # Close the serial port, even if an exception occurs
    ser.close()

