
import serial

ser = serial.Serial('COM4', 9600)  # open first serial port
print(ser.portstr)       # check which port was really used

print(ser.readline())


# print ser.name
# while True:
#     data = []
#     data.append(ser.readlines())
#     print data 
#     # further processing 
#     # send the data somewhere else etc
# print data
ser.close()




# for i in range(20):
#     response = ser.read()     # write a string
#     #response = int(response)
#     #response = float(response[0:len(response)-2].decode("utf-8"))
#     print(response)


ser.close() 