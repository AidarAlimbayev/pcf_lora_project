import threading
import queue
import time

def get_input(message, channel):
    response = input(message)
    channel.put(response)

def input_with_timeout(message, timeout):
    channel = queue.Queue()
    message = message + " [{} sec timeout] ".format(timeout)
    thread = threading.Thread(target=get_input, args=(message, channel))
    thread.daemon = True
    thread.start()

    try:
        response = channel.get(True, timeout)
        return response
    except queue.Empty:
        pass
    return None
"""
if __name__ == "__main__":
    a = '5'
    #a = input_with_timeout("Choice:", 5)
    labels = ['ararararara', 'arddddsdsdadasd', 'dddddddddddddddd']
    print(time.time())
    #time.sleep(5)

    print(type(a))
    print(a)
    if a == '1':
        print('hello')
    else: 
        print('bye')
        print(time.time())

    sec = 2
    start_time = time.time()
    stop_time = start_time + sec
    while (True):
            print('I am in while')
            
            if time.time() >= stop_time:
                break      
    labels = ['dsadasdasdasdas', 'dasdasdasdasdasd', 'asssdasdasdasdasdasd', 'ddsdsddsdssdsdsdsd', 'dssssss']
    #animal_id = max([j for i,j in enumerate(labels) if j in labels[i+1:]]) if labels != list(set(labels)) else -1
    #if animal_id is None:
    animal_id = labels[-1]
    print(animal_id)

    """

def test():

    test = '1'
    print('start')
    if test == '1':
        print('hi')
        test()
    print("bye")

test()