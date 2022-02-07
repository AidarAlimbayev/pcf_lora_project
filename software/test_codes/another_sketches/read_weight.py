import serial

weight_arr = [12,22,5,11,12,15]
# weight_signal = 125
# weight_arr.append(weight_signal)


weight_leng = len(weight_arr)
weight_all = 0
for weight in weight_arr:
    weight_all += weight

print(weight_all)

weight_ave = weight_all / weight_leng
weight_ave = '%.2f' % weight_ave
print(weight_ave)
serian_number = 12