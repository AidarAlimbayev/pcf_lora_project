
import pcf_lib
import logging

weight = 0
weight_finall = 0
date_now = ''
type_scales = "Scale_A"
row = []

 
def main():

    # add filemode="w" to overwrite
    logging.basicConfig(filename="sample_pcf.log", level=logging.INFO)
    
    
    logging.info("Program is started!")   
    weight = pcf_lib.connect_weight() 
    while(weight != 0):
        weight = pcf_lib.connect_weight() 
        if weight > 100:
            cow_id = pcf_lib.connect_id()
            logging.info("Cow is catched!")
            if cow_id != 0:
                pcf_lib.send_server(cow_id, weight_finall)
                logging.info("Data to server senden")
                pcf_lib.collect_data(cow_id, weight_finall)
                logging.info("Data is collected!")
            else:
                return 0 
                
if __name__ == "__main__":
    main()