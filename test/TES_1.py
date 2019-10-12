# import csv
# row = ['2', ' john', ' California']

# with open('people.csv', 'r') as readFile:
#     reader = csv.reader(readFile)
#     lines = list(reader)
#     lines[2] = row

# with open('people.csv', 'w') as writeFile:
#     writer = csv.writer(writeFile)
#     writer.writerows(lines)
    
# readFile.close()
# writeFile.close()

animal_id = "b'0700010101001e4b'" # Id null starting variable
null_id = "b'0700010101001e4b' " # Id null

print(null_id)
print("________")
print(animal_id)

if animal_id == null_id: # Send command to reader waiting id of animal

    print("Success")
else:
    print("Unsuccess")
            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.connect((TCP_IP, TCP_PORT))
            # s.send(bytearray([0x06, 0x00, 0x01, 0x04, 0xff, 0xd4, 0x39])) #
            # data = s.recv(BUFFER_SIZE)
            # animal_id= str(binascii.hexlify(data))
            # s.close()        