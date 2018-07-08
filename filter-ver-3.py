"""
5 Jul. 2018

ISSI, team Noa Chapal

"""

import csv
from scipy import stats

# list of inclusion and exclusion filters by column and value
incFilters = [(1,["chr10"]),(4,["T"])]
excFilters = [(6,["UTR5"])]

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

def chi_squared(n1,n2,N1,N2):
    return stats.fisher_exact([[n1,N1-n1],[n2,N2-n2]])[1]

# Part 1: Takes tab separated txt file as input and stores filtered rows in array
with open("../data/total.txt","r") as f:
    readerList = list(csv.reader(f, delimiter='\t'))
    # runs the inclusion filter (without headings) and then applies exclusion filter
    incFiltered = filter(inclusionItterator, readerList[1:])
    fullFiltered = list(filter(exclusionItterator, incFiltered))

    # applies column headings
    headings = readerList[0]

totalPositions = []
freqPositions = []

# incFilters = [(0,["smMIP_Old_P7_index17_S17"])]

# writes txt file that only contains filtered rows
with open("../data/filteredTotal.txt", "w") as f:
    writer = csv.writer(f, delimiter ="\t")
    writer.writerow(headings)
    for row in fullFiltered:
        writer.writerow(row)

# Matching elements from total to frequency
with open("../data/smMIP_Old_P7_index17_S17.sorted.rg.realigned.freq.paired.Q30.txt","r") as f:
    next(f)
    freqList = list(csv.reader(f, delimiter='\t'))
filteredTotal = list(filter(lambda x: x[0]=='smMIP_Old_P7_index17_S17', fullFiltered))
filteredTotalPositions = [row[2] for row in filteredTotal]
filteredFreq = list(filter(lambda x: x[1] in filteredTotalPositions, freqList))

print(len(filteredTotalPositions))
print(len(filteredFreq))

mutations = {
    'A': [6,7],
    'C': [8,9],
    'T': [10,11],
    'G': [12,13]
}

filteredTotalChi = []
k = 0
i = 0

# fix for duplicate totals
while i in range(0,len(filteredTotal)):
    j = i - k
    print(len(filteredFreq))
    if j == len(filteredFreq):
        print('j: '+j)
    if filteredTotal[i][2] == filteredFreq[j]:
        mut = mutations[filteredTotal[j][6]]
        chi_squared = chi_squared(filteredFreq[j][mut[0]],filteredFreq[j][mut[1]],filteredFreq[j][4],filteredFreq[j][5])
        filteredTotalChi.append(filteredTotal.append(chi_squared))
        i += 1
    else:
        k += 1

with open("../data/filteredTotal.txt", "w") as f:
    writer = csv.writer(f, delimiter ="\t")
    writer.writerow(headings)
    for row in fullFiltered:
        writer.writerow(row)

with open("../data/filteredTotalChi.txt","w") as f:
    writer = csv.writer(f, delimiter ="\t")
    # writer.writerow(headings.append("p"))
    for row in filteredTotalChi:
        writer.writerow(row)
