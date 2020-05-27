import main_pcf_lib2 as pcf

type_scales = "Scale_A" # Тип весов. Дано на каждые весы по отдельности
cow_id = "b'0700010101001e4b'" # Значение пустого ответа от считывателя 
null_id = "b'0700010101001e4b'"
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
       
    while(True):
        
        cow_id = pcf.Connect_RFID_reader()
        #print("Cow ID: ")
        #print(cow_id)
            
        if cow_id != '070106156079':
            #print()
            weight_finall = pcf.Connect_ARD_get_weight(cow_id, s)
            
            if float(weight_finall) != 0:
                pcf.Collect_data_CSV(cow_id, weight_finall, type_scales)
                pcf.Send_data_to_server(cow_id, weight_finall, type_scales)
            else:
                return 0

main()
