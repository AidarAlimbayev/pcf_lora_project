#connect_weight.py

def connect_weight():
    weight_list = []
    print("Measure weight of cow")
    weight = float(input("Enter weight: "))
    while (float(weight) != 0):
        weight = float(input("Enter weight:___"))
        weight_list.append(float(weight))
    if weight_list == 0 or weight_list == []:
        return(0)
    else:
        if weight_list != 0:
            print ("Weight list: ", weight_list)
            del weight_list[-1]

        weight_finall =  sum(weight_list) / len(weight_list) 
        weight_list = []
        return(weight_finall)