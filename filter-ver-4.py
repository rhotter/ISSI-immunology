"""
5 Jul. 2018

ISSI, team Noa Chapal

"""

import csv
from scipy import stats

# list of inclusion and exclusion filters by column and value
incFilters = [(9,["nonsynonymous SNV"]),(6,["exonic"])]
excFilters = []
depth = 1500
vaf = [0.02,0.4]
cutOffP = 0.05

# itterates through filters and return true if value corresponds in column
def inclusionItterator(x):
    for filt in incFilters:
        if x[filt[0]] not in filt[1]:
            return False
    return True

def exclusionItterator(x):
    for filt in excFilters:
        if x[filt[0]] in filt[1]:
            return False
    return True

def chi_squaredFunc(n1,n2,N1,N2,c):
    if N1 == 0 and N2 == 0:
        return -2
    if n1 < 0 or N1-n1 < 0 or n2 < 0 or N2-n2 < 0:
        return -1
    else:
        return stats.fisher_exact([[n1,N1-n1],[n2,N2-n2]])[1]

# Part 1: Takes tab separated txt file as input and stores filtered rows in array
with open("../data/total.txt","r") as f:
    readerList = list(csv.reader(f, delimiter='\t'))
    # runs the inclusion filter (without headings) and then applies exclusion filter
    incFiltered = filter(inclusionItterator, readerList[1:])
    depthFiltered = filter(lambda x:int(x[19]) >= depth, incFiltered)
    vafFiltered = filter(lambda x: float(x[21]) >= vaf[0] and float(x[21]) <= vaf[1], depthFiltered)
    fullFiltered = list(filter(exclusionItterator, vafFiltered))

    # applies column headings
    headings = readerList[0]

totalPositions = []
freqPositions = []

# incFilters = [(0,["smMIP_Old_P7_index17_S17"])]

# writes an array of filtered indeces
patientTitles = []
lastPatient = []
for row in fullFiltered:
    if row[0] != lastPatient:
        lastPatient = row[0]
        patientTitles.append(lastPatient)

# Matching elements from total to frequency
mutations = {
    'A': [6,7],
    'C': [8,9],
    'T': [10,11],
    'G': [12,13]
}
filteredTotalChi = []

for patient in patientTitles:
    try:
        with open("../data/frequencyFiles/" + patient + ".sorted.rg.realigned.freq.paired.Q30.txt","r") as f:
            next(f)
            freqList = list(csv.reader(f, delimiter='\t'))
        filteredTotal = list(filter(lambda x: x[0] == patient, fullFiltered))
        filteredTotal = sorted(filteredTotal, key = lambda x: x[2])
        filteredTotalPositions = [row[2] for row in filteredTotal]
        filteredFreq = list(filter(lambda x: x[1] in filteredTotalPositions, freqList))
        filteredFreq = sorted(filteredFreq, key = lambda x: x[1])

        k = 0
        i = 0

        lastTrue = False
        # fix for duplicate totals
        while i in range(0,len(filteredTotal)):
            j = i - k

            # print(i,j)
            # print(filteredTotal[i][2])

            # resolves index issue at the end of array
            if lastTrue and j >= len(filteredFreq)-1:
                k += 1
                j = i - k

            # assumes unique nucleotide positions in Total file
            if filteredTotal[i][2] == filteredFreq[j][1]:
                mut = mutations[filteredTotal[j][5]]
                chi_squared = chi_squaredFunc(int(filteredFreq[j][mut[0]]),
                                              int(filteredFreq[j][mut[1]]),
                                              int(filteredFreq[j][4]),
                                              int(filteredFreq[j][5]),
                                              filteredTotal[i][2])
                if chi_squared == -1 or (chi_squared != -2 and chi_squared >= cutOffP):
                    filteredTotalChi.append(filteredTotal[i]+[str(chi_squared)])
                i += 1
                lastTrue = True
            else:
                k += 1
                lastTrue = False
    except IOError:
        print("frequency file missing for: " + patient)



with open("../data/filteredTotalChi.txt","w") as f:
    writer = csv.writer(f, delimiter ="\t")
    writer.writerow(headings +['p'])
    for row in filteredTotalChi:
        writer.writerow(row)
