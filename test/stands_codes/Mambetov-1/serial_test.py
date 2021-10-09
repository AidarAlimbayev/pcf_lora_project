
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)  # open first serial port
end = 1

while (end != 0):
    print(ser.portstr)      # check which port was really used
    print("_________")
    print(ser.readline())
    print("_________")
    #end = input()



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
