# Removes duplciates from frequency file

import csv

with open("../data/smMIP_Old_P7_index17_S17.sorted.rg.realigned.freq.paired.Q30.txt","r") as f:
    readerList = list(csv.reader(f, delimiter='\t'))

readerList = sorted(readerList, key = lambda x: x[1])

previous = []
i = 0
while i in range(0,len(readerList)):
    if readerList[i][1] == previous:
        print('dup')
        readerList.pop(i)
    previous = readerList[i][1]
    i += 1


with open("../data/newFrequency.txt","w") as f:
    writer = csv.writer(f, delimiter = "\t")
    for row in readerList:
        writer.writerow(row)
