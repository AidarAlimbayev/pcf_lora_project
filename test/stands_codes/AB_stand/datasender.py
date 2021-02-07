#!/usr/bin/sudo python3

def Send_data_to_server(animal_id, weight_finall, type_scales): # Отправка данных на сервер КАТУ по JSON
    try:
        df = open('cow_database', 'r')


    
    try:
        print("lib:RFID_reader: Start sending DATA TO SERVER:")
        logging.info("lib:RFID_reader: Start sending DATA TO SERVER:")
        url = 'http://194.4.56.86:8501/api/weights'
        headers = {'Content-type': 'application/json'}
        data = {"AnimalNumber" : animal_id,
                "Date" : str(datetime.now()),
                "Weight" : weight_finall,
                "ScalesModel" : type_scales}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        logging.info("lib:RFID_reader: Answer from server: ")
        logging.info(answer) # можно ли как-то на этой строке остановиться вдебаге?
        print("lib:RFID_reader: Answer from server: ")
        print(answer)
    except Exception as e:
        logging.info("lib:RFID_reader: Err send data to server")
        logging.info(e)
    else:
        logging.info("lib:RFID_reader: 4 step send data")
        logging.info("lib:RFID_reader: End of the cycle")