import csv
import matplotlib.pyplot as plt
import plotly.plotly as py
from filter2 import patientsPositions

mutationsCounts = []
type = ""

with open("../data/sample_ids.txt", "r") as f:
    readerList = list(csv.reader(f, delimiter='\t'))
    for row in readerList:
        for patient in patientsPositions:
            if row[0] == patient[0]:
                mutationsCounts.append([row[2], patient[0], len(patient) - 1])

with open("../data/mutationCounts.txt", "w") as f:
    writer = csv.writer(f, delimiter="\t")
    for row in mutationsCounts:
        writer.writerow(row)
print(mutationsCounts)