import main_pcf_lib as pcf

type_scales = "Scale_A" # Тип весов. Дано на каждые весы по отдельности
cow_id = "b'0700010101001e4b'" # Значение пустого ответа от считывателя 
weight_finall = 0

# Часть кода для первого подключения к Ардуино
try:
    s = pcf.serial.Serial('/dev/ttyACM0',9600) 
except Exception as e:
    print("Ошибка подключения к Ардуино, нету файла /dev/ttyACM0")
    print(e)
else:
    print("Arduino подключено успешно")




def main():
    print ("Start script")
    try: 
        cow_id = "b'0700010101001e4b'"
        weight_finall = pcf.Connect_ARD_get_weight(cow_id, s)
    except Exception as e:
        print(e)
        print("Ошибка подключения к Ардуино 1")
    else:
        print("1 step rfid")
    
    #cow_id = 1 # Проверочная переменная для тестирования исключений

    while(weight_finall != 0):
        try: 
            #print("1.2 step connect to Arduino weight measure")
            weight_finall = pcf.Connect_ARD_get_weight(cow_id, s)
        except Exception as e:
            print(e)
            print("Ошибка подключения к Ардуино 2")
        else:
            print("1 step rfid")
            #print(cow_id)
            #print(weight_finall)
            
        if cow_id != 0:
            
            try:
                #print("1.3 step connect to RFID reader to get id")
                cow_id = pcf.Connect_RFID_reader()
            except Exception as e:
                print(e)
                print("Ошибка подключения к RFID reader")
            else: 
                print ("2 step RFID")
            
            #weight_finall = 1 # Проверочная переменная для тестирования исключений

            if float(weight_finall) != 0:
                
                try: 
                    print(cow_id)
                    print(weight_finall)
                    print(type_scales)                    
                    pcf.Collect_data_CSV(cow_id, weight_finall, type_scales)
                except Exception as e:
                    print(e)
                    print("Ошибка записи данных в файл")
                else:
                    print ("3 step collect data")   

                try:
                    pcf.Send_data_to_server(cow_id, weight_finall, type_scales)
                except Exception as e:
                    print(e)
                    print("Ошибка передачи данных на сервер")
                else:
                    print ("4 step send data")
                    print ("End of the cycle")

            else:
                return 0

main()
