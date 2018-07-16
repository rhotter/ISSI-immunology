# Removes duplciates from frequency file

import csv

# Get patientTitles

freqPath = '/home/labs/shlush/barakor/barakor_temp/arch3_freq/reposed/polished/'
totalPath = '/home/labs/shlush/shared/Noa/LTR_July2018/NSR6_total.txt'
newFreqPath = '/home/labs/shlush/shared/Noa/LTR_July2018/newFreq/'

with open(totalPath,"r") as f:
    readerList = list(csv.reader(f, delimiter='\t'))
paths = []
lastPatient = []
for row in readerList:
    if row[0] != lastPatient:
        lastPatient = row[0]
        paths.append(lastPatient + ".sorted.rg.realigned.freq.paired.Q30.rmbg.txt")

for path in paths:
    readPath = freqPath + path 
    with open(readPath,"r") as f:
        readerList = list(csv.reader(f, delimiter='\t'))
        headings = readerList[0]

    readerList = sorted(readerList[1:], key = lambda x: x[1])

    previous = []
    i = 0
    newReaderList = []
    while i in range(0,len(readerList)):
        if readerList[i][1] != previous:
            newReaderList.append(readerList[i])
        previous = readerList[i][1]
        i += 1

    writePath = newFreqPath + path
    with open(writePath,"w") as f:
        writer = csv.writer(f, delimiter = "\t")
        writer.writerow(headings)
        for row in newReaderList:
            writer.writerow(row)
