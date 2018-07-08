# Removes duplciates from frequency file

import csv
paths = ["../data/smMIP_Old_P7_index17_S17.sorted.rg.realigned.freq.paired.Q30.txt",
         "../data/smMIP_Old_P7_index17_S17.sorted.rg.realigned.freq.paired.Q30.txt",
         "../data/smMIP_Old_P7_index17_S17.sorted.rg.realigned.freq.paired.Q30.txt",
         "../data/smMIP_Old_P7_index17_S17.sorted.rg.realigned.freq.paired.Q30.txt"]
for path in paths:
    with open(path,"r") as f:
        readerList = list(csv.reader(f, delimiter='\t'))
        headings = readerList[0]

    readerList = sorted(readerList[1:], key = lambda x: x[1])

    previous = []
    i = 0
    while i in range(0,len(readerList)):
        if readerList[i][1] == previous:
            readerList.pop(i)
        previous = readerList[i][1]
        i += 1

    with open(path,"w") as f:
        writer = csv.writer(f, delimiter = "\t")
        writer.writerow(headings)
        for row in readerList:
            writer.writerow(row)
