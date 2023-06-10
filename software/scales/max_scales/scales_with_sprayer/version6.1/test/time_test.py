
import time

def timer():
    next_time = time.time()+1    
    count = 0
    while(count < 5):
        current_time = time.time()
        now = next_time - current_time
        if now < 0:   
            if round(time.time(), 0)%5 == 0:
                count+=1
                print(count)
            next_time=time.time()+1

timer()