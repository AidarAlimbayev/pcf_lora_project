import main_pcf_lib

type_scales = "Scale_A"
s = serial.Serial('/dev/ttyACM0',9600)


def main():
    print ("1 step rfid")
    
    cow_id = main_pcf_lib.Connect_ARD_get_weight()
    while(cow_id != 0)
        cow_id = main_pcf_lib.Connect_ARD_get_weight()
        if cow_id != "b'0700010101":
            print ("2 step weight")
            weight_finall = main_pcf_lib.Connect_ARD_get_weight())
            if float(weight_finall) != 0:
                print ("3 step collect data")
                main_pcf_lib.Collect_data_CSV(cow_id, weight_finall, type_scales)
                print ("4 step send data")
                main_pcf_lib.Send_data_to_server(cow_id, weight_finall, type_scales)
            else:
                return 0

main()
