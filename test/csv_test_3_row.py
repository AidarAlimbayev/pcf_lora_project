import csv

row = ['4', 'KZC154000004', '2019-08-19T21:22:22:54', '284', 'type_A'] #3,KZC154000003,2019-08-19T21:22:22:54,283,type_A

with open('cows.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(row)

csvFile.close()