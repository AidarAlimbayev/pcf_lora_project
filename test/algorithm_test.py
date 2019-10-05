from datetime import datetime, date, time


id = 0
weight_list = []
weight = 0
date_now = str(datetime.now())

def connect_weight():
    print("Measure weight of cow")
    weight = input("Enter weight: ")
    if weight != 0:
        weight = input("Enter weight:_")
        weight_list.append(weight)
        #connect_weight()
    else: 
        print("Array:", weight_list)
        return(0)
    

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