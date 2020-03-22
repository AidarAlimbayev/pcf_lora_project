
import pcf_lib

weight = 0
weight_finall = 0
date_now = ''
type_scales = "Scale_A"
row = []

 
def main():

    pcf_lib.logging_start()
        
    cow_id = pcf_lib.connect_id()
    while(cow_id != 0):
        cow_id = pcf_lib.connect_id()
        if float(cow_id) != 0:
            weight_finall = pcf_lib.connect_weight()
            if float(weight_finall) != 0:
                pcf_lib.send_server(cow_id, weight_finall)
                pcf_lib.collect_data(cow_id, weight_finall)
            else:
                return 0 

main()