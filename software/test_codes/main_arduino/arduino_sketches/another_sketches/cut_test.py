# test cut python

animal_id = "123456789" # Id null starting variable
#null_id = "b'0700010101001e4b'"

print("Received ID cow: ")
print(animal_id)
        
#animal_id_new = animal_id[:-5] # cut from back [1234*****<-]
#animal_id_new = animal_id[:3] # cut from begin [123******<-]
#animal_id_new = animal_id[3:] # cut from begin [->***456789]
animal_id_new = animal_id[-3:] # cut from begin [->*****789]

#animal_id_new = animal_id[:] # cut from begin
#animal_id_new = animal_id_new[-2:]
        
print("CUT ID cow: ")
print(animal_id_new)