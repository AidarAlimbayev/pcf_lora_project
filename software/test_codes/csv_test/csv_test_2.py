import csv

#i = 4;

row = ['4', 'KZC154000004', '2019-08-19T21:22:22:54', '284', 'type_A'] #3,KZC154000003,2019-08-19T21:22:22:54,283,type_A
name = ['88', 'qwe', 'weee']
# with open('cows.csv', 'r') as readFile:
#     reader = csv.reader(readFile)
#     lines = list(reader)
#     lines.append(name)
#     print(lines)

with open('cows.csv', 'a', newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(name)

#readFile.close()
writeFile.close()