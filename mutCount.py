import csv

with open("../data/NSR6_filteredTotal_dp0.txt","r") as f:
    readerList = list(csv.reader(f, delimiter='\t'))



patientTitles = []
lastPatient = []
for row in readerList:
    if row[0] != lastPatient:
        lastPatient = row[0]
        patientTitles.append(lastPatient)

mutationsCounts = []
type = ""

with open("../data/sample_ids.txt", "r") as f:
    readerList = list(csv.reader(f, delimiter='\t'))
    for row in readerList:
        for patient in patientTitles:
            if row[0] == patient:
                mutationsCounts.append([row[2], patient, len(patient) - 1])

with open("../data/mutationCountsNSR6.txt", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    for row in mutationsCounts:
        writer.writerow(row)
