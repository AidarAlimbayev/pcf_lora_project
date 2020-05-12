import main_pcf_lib as pcf

type_scales = "Scale_A"
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
        cow_id = pcf.Connect_ARD_get_weight()
    except Exception as e:
        print(e)
        print("Ошибка подключения к Ардуино")
    else:
        print("1 step rfid")
    
    #cow_id = 1 # Проверочная переменная для тестирования исключений

    while(cow_id != 0):
        try: 
            cow_id = pcf.Connect_ARD_get_weight()
        except Exception as e:
            print(e)
            print("Ошибка подключения к Ардуино")
        else:
            print("1 step rfid")
            
        if cow_id != "b'0700010101":
            
            try:
                weight_finall = pcf.Connect_ARD_get_weight()
            except Exception as e:
                print(e)
                print("Ошибка подключения к Ардуино ")
            else: 
                print ("2 step weight")
            
            #weight_finall = 1 # Проверочная переменная для тестирования исключений

            if float(weight_finall) != 0:
                
                try: 
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

            else:
                return 0

main()
