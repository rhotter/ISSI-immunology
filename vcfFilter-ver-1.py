import csv

newTable = []

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

def getValue(list,name):
    for i in range(0, len(info)):
        if name in list[i]:
            value = [list[i].split('=')[1]]
            return value


# Get patientTitles
with open("../data/total.txt","r") as f:
    readerList = list(csv.reader(f, delimiter='\t'))
patientTitles = []
lastPatient = []
for row in readerList:
    if row[0] != lastPatient:
        lastPatient = row[0]
        patientTitles.append(lastPatient)

vcfDict = {
    'platypus': {
        'NR': 4,
        'NV': 5,
        'DP': 3,
        'minDP': 0
    },
    'varscan': {
        'NR': 4,
        'NV': 5,
        'DP': 3,
        'minDP': 0
    }
}

initialHeadingSize = 10

for patient in patientTitles:
    for vcfType in ['platypus','varscan']:
        newTable = []
        # Generate array with relevant VCF
        try:\

            # 141455_004_S2_L001.sorted.rg.realigned.varscan.reposed.annovar.vcf.hg19_multianno
            with open("../data/vcf/" + patient + ".sorted.rg.realigned." + vcfType + ".annovar.vcf.hg19_multianno.vcf","r") as f:
                readerList = list(csv.reader(f, delimiter='\t'))
                start = False
                # needs to be cleaned up
                readerListLength = len(readerList)
                i = 0

                # Find start
                while i in range(0,readerListLength):
                    if readerList[i][0] == '#CHROM':
                        row = readerList[i]
                        start = i + 1
                        heading = row + ['vaf'] + ['isExonic'] + ['depth']
                    i += 1

                for i in range(start,readerListLength):
                    row = readerList[i]
                    data = row[9].split(':')
                    info = row[7].split(';')
                    NR = int(data[vcfDict[vcfType]['NR']])
                    NV = int(data[vcfDict[vcfType]['NV']])
                    DP = [int(data[vcfDict[vcfType]['DP']])]

                    isExonic = getValue(info, "ExonicFunc.refGene=")

                    try:
                        vaf = [NV/NR]
                    except ZeroDivisionError:
                        vaf = [-1]

                    newTable.append(row + vaf + isExonic + DP)

            columns = {
                'vaf': initialHeadingSize,
                'isExonic': initialHeadingSize + 1,
                'depth': initialHeadingSize + 2
            }

            incFilters = [(columns['isExonic'],[".",'exonic'])]
            excFilters = []
            vaf = [0.02,0.4]
            minDepth = vcfDict[vcfType]['minDP']

            incFiltered = filter(inclusionItterator, newTable)
            depthFiltered = filter(lambda x: int(x[columns['depth']]) >= minDepth, incFiltered)
            vafFiltered = filter(lambda x: float(x[columns['vaf']]) >= vaf[0] and float(x[columns['vaf']]) <= vaf[1], depthFiltered)
            fullFiltered = list(filter(exclusionItterator, vafFiltered))

            # vafFiltered = filter(lambda x: float(x[9]) >= vaf[0] and float(x[9]) <= vaf[1], readerList)

            with open("../data/vcf/filtered/" + patient + ".sorted.rg.realigned." + vcfType + ".annovar.vcf.hg19_multianno-filtered.txt","w") as f:
                writer = csv.writer(f, delimiter ="\t")
                writer.writerow(heading)
                for row in fullFiltered:
                    writer.writerow(row)

        except IOError:
            print('No file for ' + patient + ' ' + vcfType)
