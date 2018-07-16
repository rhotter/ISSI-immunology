"""
5 Jul. 2018

ISSI, team Noa Chapal

"""

import csv, re
from scipy import stats

# list of inclusion and exclusion filters by column and value
incFilters = [(9,["nonsynonymous SNV", "stopgain", "stoploss"]),(6,["exonic"])]
excFilters = [(7,["SMC3", "CBL", "PPM1D", "STAG2", "WT1", "NOTCH1", "SMC1A", "CLAR", "NPM1", "PTPN11", "CEBPA"])]
acidFilters = [("SRSF2", "P95H", "P95R", "P95L"),("U2AF1", "34",  "157"), ("U2AF1", "34", "157"), ("SF3B1", "625", "666", "700"), ("SETBP1", "858-871"), ("NRAS", "12", "13", "61"), ("KRAS", "12", "13"), ("IDH1", "132"), ("IDH2", "140", "172"), ("FLT3", "835"), ("MYD88", "L265P"), ("KIT", "815"), ("MPL", "515"), ("BRAF", "600"), ("JAK2", "617")]

# depth = 1500
vaf = [0.02,0.4]
cutOffP = 0.05

depth = 1500
# vaf = [-10,10]
# cutOffP = -10

freqPath = '/home/labs/shlush/shared/Noa/LTR_July2018/newFreq/'
totalPath = '/home/labs/shlush/shared/Noa/LTR_July2018/NSR5_total.txt'
writePath = '/home/labs/shlush/shared/Noa/LTR_July2018/NSR5/NSR5_filteredTotal_dp1500.txt'

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

def acidItterator(x):
    totalGeneInfo = x[10]
    if 'p.' in totalGeneInfo:
        for acidFilt in acidFilters:
            gene = acidFilt[0]
            totalGene = x[7]
            if gene in totalGene:
                for acid in acidFilt[1:]:
                    if acid.isdigit():
                        searchy = r'p.[A-Z]%s[A-Z]' % acid 
                        if re.search(searchy,totalGeneInfo) != None:
                            return True
                    else:
                        splitAcid = acid.split('-')
                        if len(splitAcid) == 2:
                            searchy = r'p.[A-Z][%s-%s][A-Z]' % (splitAcid[0],splitAcid[1])
                            if re.search(searchy,totalGeneInfo) != None:
                                return True
                        elif 'p.' + acid in totalGeneInfo:
                            return True
                return False
        return True
    else:
        return True

def chi_squaredFunc(n1,n2,N1,N2):
    if N1 == 0 and N2 == 0:
        return -2
    if n1 < 0 or N1-n1 < 0 or n2 < 0 or N2-n2 < 0:
        return -1
    else:
        return stats.fisher_exact([[n1,N1-n1],[n2,N2-n2]])[1]

# Part 1: Takes tab separated txt file as input and stores filtered rows in array
with open(totalPath,"r") as f:
    readerList = list(csv.reader(f, delimiter='\t'))
    incFiltered = filter(inclusionItterator, readerList[1:])
    excFiltered = filter(exclusionItterator, incFiltered)
    depthFiltered = filter(lambda x:int(x[19]) >= depth, excFiltered)
    vafFiltered = filter(lambda x: float(x[21]) >= vaf[0] and float(x[21]) <= vaf[1], depthFiltered)
    fullFiltered = list(filter(acidItterator, vafFiltered))

    # fullFiltered = list(filter(exclusionItterator, readerList))

    
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

count = 1
size = len(patientTitles)
for patient in patientTitles:
    print(str(count) + '/' + str(size))
    count += 1
    try:
        with open(freqPath + patient + ".sorted.rg.realigned.freq.paired.Q30.rmbg.txt","r") as f:
            next(f)
            freqList = list(csv.reader(f, delimiter='\t'))
        filteredTotal = list(filter(lambda x: x[0] == patient, fullFiltered))

        filteredTotal = sorted(filteredTotal, key = lambda x: x[2])

        # remove duplicates from filteredTotal
        previous = ()
        previousDepth = -1
        filteredTotalNoDups = []
        j = 0
        for row in filteredTotal:
            current = (row[2], row[4], row[5])
            currentDepth = row[19]
            if current != previous:
                previous = (row[2], row[4], row[5])
                previousDepth = row[19]
                filteredTotalNoDups.append(row)
                j += 1
            elif previousDepth < currentDepth:
                # keep current
                previousDepth = row[19]
                filteredTotalNoDups.append(row)
                filteredTotalNoDups.pop(j-1)

       

        filteredTotalPositions = [row[2] for row in filteredTotalNoDups]
        filteredFreq = list(filter(lambda x: x[1] in filteredTotalPositions, freqList))
        filteredFreq = sorted(filteredFreq, key = lambda x: x[1])
        k = 0
        i = 0

    
        # fix for duplicate totals
        lastTrue = False
        while i in range(0,len(filteredTotalNoDups)):
            j = i - k


            # resolves index issue at the end of array
            if lastTrue and j > len(filteredFreq)-1:
                k += 1
                j = i - k
            # assumes unique nucleotide positions in Total file
            if filteredTotalNoDups[i][2] == filteredFreq[j][1]:
                mut = mutations[filteredTotalNoDups[i][5]]
                chi_squared = chi_squaredFunc(int(filteredFreq[j][mut[0]]),
                							  int(filteredFreq[j][mut[1]]),
                							  int(filteredFreq[j][4]),
                							  int(filteredFreq[j][5]))
                if chi_squared == -1 or (chi_squared != -2 and chi_squared >= cutOffP):
                    filteredTotalChi.append(filteredTotalNoDups[i]+[str(chi_squared)])
                i += 1
                lastTrue = True
            else:
                k += 1
                lastTrue = False
    except IOError:
        print("frequency file missing for: " + patient)


with open(writePath,"w") as f:
    writer = csv.writer(f, delimiter ="\t")
    #writer.writerow(headings +['p'])
    for row in filteredTotalChi:
        writer.writerow(row)
