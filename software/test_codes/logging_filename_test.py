from datetime import datetime, date, time


print(datetime.date(datetime.now()),"_",datetime.time(datetime.now()))
print("_____")
print(datetime.now().strftime("%Y_%m_%d_%H:%M:%S"))

