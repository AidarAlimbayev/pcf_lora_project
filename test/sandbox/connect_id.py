#connect_id.py

def connect_id():
    print("Try to connect RFID")
    cow_id = str(input("Enter ID: "))
    if cow_id == 0:
        connect_id()
    else:
        return(cow_id)