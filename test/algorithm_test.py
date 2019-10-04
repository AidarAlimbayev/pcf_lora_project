from datetime import datetime, date, time


id = 0
weight = 0
date_now = str(datetime.now())

def connect_weight():
    print("Measure weight of cow")
    weight = input("Enter weight: ")
    if weight == 0 :
        mark = 0
        connect_weight()
    elif weight != 0:
        mark = 1
        connect_weight()
    elif mark == 1 and weight == 0:
        mark = 0
        return(weight)

def connect_id():
    print("Try to connect RFID")
    id = input("Enter ID: ")
    if id == 0:
        connect_id()
    else:
        return(id)

connect_weight()

#id = connect_id()

#print(id)