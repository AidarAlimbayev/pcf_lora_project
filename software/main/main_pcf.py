#!/usr/bin/sudo python
# pre version 4.5 Aidar edition
import lib_pcf as pcf

pcf.time.sleep(10) # sleep time for connection to serial library


# config of equipment and contacts
#old variable type_scales -> new variable equipment_name (must be unique)
<<<<<<< HEAD
type_scales = "pcf_model_5" # equipment_name 
=======
type_scales = "pcf_model_6" # equipment_name 
>>>>>>> 5b14a03 (new spray)
type = "SCALES"
model = "800"
location = 'SHOS'
person = 'Sergey'
contact = '+77053209585'


# null values for variables
animal_id = "b'435400040001'" # value of null answer of RFID reader
null_id = "b'435400040001'"
weight_finall = 0
duration = 10

# Connection to arduino
try:
    s = pcf.serial.Serial('/dev/ttyACM0',9600) # path inside rapberry pi to arduino into dev folder
    pcf.print_log("Connect arduino", s.name)
    pcf.print_log("Configuration of serial: ", s)
except Exception as e:
    pcf.print_log("Error to connection to arduino, there is no file: /dev/ttyACM0", e)
else:
    pcf.print_log("Success: Arduino connected")

# Add equipment type, name, location, person and contacts, 
try:
    pcf.print_log("Start to add unique equipment in database")
    pcf.Insert_New_Unique_Equipment_Type_Model(type, model, type_scales, location, person, contact)
except Exception as e:
    pcf.print_log("Error in addting unique equipment in database", e)
else:
    pcf.print_log("Success: Unique equipment added to database")

def main():
    pcf.print_log("Start main script")

    while(True):
        pcf.print_log("Infinite cycle")
        animal_id = pcf.Connect_RFID_reader() # Connection to RFID reader 
        pcf.print_log("First step cow ID :", animal_id)

        pcf.time.sleep(1) # sleep to decrease workload and deccrease tmperature of CPU
        
        if animal_id != '435400040001': # Comparision to null animal_id answer 
            # second ID is also null 
            pcf.print_log("After read cow ID :", animal_id)
            pcf.Insert_New_Unique_Animal_ID(animal_id)
                        
<<<<<<< HEAD
            weight_finall = pcf.Connect_ARD_get_weight(animal_id, s, type_scales) # Grab weight from arduino and collect to weight_finall
=======
            weight_finall, drink_duration = pcf.Connect_ARD_get_weight(animal_id, s, type_scales) # Grab weight from arduino and collect to weight_finall
>>>>>>> 5b14a03 (new spray)
            pcf.print_log("main: weight_finall", weight_finall)

            if str(weight_finall) > '0':
                pcf.print_log("main: Collect data")
                pcf.Collect_data_CSV(animal_id, weight_finall, type_scales) # Save weight data into CSV file

                pcf.print_log("main: Collect data to main database")
<<<<<<< HEAD
                pcf.Collect_to_Main_Data_Table(animal_id, weight_finall, type_scales)
=======
                pcf.Collect_to_Main_Data_Table(animal_id, weight_finall, type_scales, drink_duration)
>>>>>>> 5b14a03 (new spray)
                
                #pcf.print_log("main: Spray ")
                #pcf.Spray_Animal_by_Spray_Status(animal_id, duration)

                pcf.print_log("main: Send data to server")
                pcf.Send_data_to_server(animal_id, weight_finall, type_scales) # Send data to server by JSON post request

                #if check_internet_connection() == True :
                    #pcf.Send_data_to_server_from_sqlite()
                # pcf.
                # cutter 

<<<<<<< HEAD
main()
=======
main()
>>>>>>> 5b14a03 (new spray)
