"""
5 Jul. 2018

ISSI, team Noa Chapal

"""

import csv
from scipy import stats

# list of inclusion and exclusion filters by column and value
# incFilters = [(1,["chr10"]),(4,["T"])]
# excFilters = [(6,["UTR5"])]
incFilters=[]
excFilters=[]


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
with open("../data/frequencyFiles/smMIP_Old_P7_index17_S17.sorted.rg.realigned.freq.paired.Q30.txt","r") as f:
    next(f)
    freqList = list(csv.reader(f, delimiter='\t'))
filteredTotal = list(filter(lambda x: x[0]=='smMIP_Old_P7_index17_S17', fullFiltered))
filteredTotal = sorted(filteredTotal, key = lambda x: x[2])
filteredTotalPositions = [row[2] for row in filteredTotal]
filteredFreq = list(filter(lambda x: x[1] in filteredTotalPositions, freqList))
filteredFreq = sorted(filteredFreq, key = lambda x: x[1])

# with open("../data/freqList.txt","w") as f:
#     writer = csv.writer(f, delimiter ="\t")
#     for row in freqList:
#         writer.writerow(row)
#
# with open("../data/filteredTotalPositions.txt","w") as f:
#     writer = csv.writer(f, delimiter ="\t")
#     for row in filteredTotalPositions:
#         writer.writerow(row)
#
# with open("../data/filteredFreq.txt","w") as f:
#     writer = csv.writer(f, delimiter ="\t")
#     for row in filteredFreq:
#         writer.writerow(row)

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
    if j < 0:
        print(i,j)
        print(filteredTotal[i][2])

    # assumes unique nucleotide positions in Total file
    if filteredTotal[i][2] == filteredFreq[j][1]:
        mut = mutations[filteredTotal[j][5]]
        chi_squared = chi_squaredFunc(int(filteredFreq[j][mut[0]]),
                                      int(filteredFreq[j][mut[1]]),
                                      int(filteredFreq[j][4]),
                                      int(filteredFreq[j][5]),
                                      filteredTotal[i][2])
        if chi_squared == -2:
            filteredTotalChi.append(filteredTotal[i]+[str(chi_squared)])
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
    writer.writerow(headings +['p'])
    for row in filteredTotalChi:
        writer.writerow(row)
