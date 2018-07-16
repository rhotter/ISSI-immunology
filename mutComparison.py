import csv

preList = []
tempList = []
results = []
healthy = []
shared = []
sick = []
idList = []
patients = []
healthList = []
totalHealthy = 0
m = 0
n = 0

with open("../data/NSR5_filteredTotal_dp1500.txt","r") as f:
    readerList = list(csv.reader(f, delimiter='\t'))
with open("../data/sample_ids.txt","r") as f:
    patientList = list(csv.reader(f, delimiter='\t'))
    for row in readerList:
        tempList.append(row [3:6])
    for i in range(len(readerList)):
        for j in range(len(readerList)):
                if(i != j):
                    if(tempList[i] == tempList[j]):
                        if( not i in results):
                            results.append(i)
    for row in patientList:
        healthList.append(row [2])
    for row in patientList:
        preList.append(row [0])
    for row in readerList:
        idList.append(row [0])
    for k in range(len(patientList)):
        for g in range(len(readerList)):
            if (preList[k] == idList[g]):
                if(not k in patients):
                    patients.append(k)



with open("../data/sharedmut.txt","w") as f:
    writer = csv.writer(f, delimiter = '\t')
    for i in results:
        writer.writerow(readerList[i])

with open("../data/sharedMutDetailed.txt","w") as f:
    writer2 = csv.writer(f, delimiter = '\t')
    for k in patients:
        writer2.writerow(patientList[k])

with open("../data/sharedMutDetailed.txt","r") as f:
    readList = list(csv.reader(f, delimiter='\t'))
for row in readList:
    if (row[2]) == "Healthy":
        sharedHealthy = m + 1
        m += 1
    else:
        sharedSick = n + 1
        n += 1

with open("../data/sharedMutNum.txt", "w") as f:
    writer3 = csv.writer (f, delimiter = '\t')
    writer3.writerow([sharedSick] + [sharedHealthy])
