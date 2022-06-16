cow_id_new = '0'
additional_id_cow = '1'

if (cow_id_new != '0') or (additional_id_cow != '1'):
    print("cow_id_new != 0 or additional_id_cow != 1")

elif (cow_id_new != '1') or (additional_id_cow != '1'): 
    print("cow_id_new == 1 or additional_id_cow == 1")

elif (cow_id_new != '1') and (additional_id_cow != '0'): 
    print("cow_id_new != 1 and additional_id_cow != 0")

elif (cow_id_new != '0') and (additional_id_cow != '1'): 
    print("cow_id_new != 0 and additional_id_cow != 1")

else:
    print("everything is gone")