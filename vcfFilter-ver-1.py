import csv

newTable = []
vcfType = ""

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
        'NV': 5
    },
    'varscan': {
        'NR': 4,
        'NV': 5
    }
}

initialHeadingSize = 10

for patient in patientTitles:
    for vcfType in ['platypus','varscan']:
        # Generate array with relevant VCF
        try:
            with open("../data/vcf/" + patient + ".sorted.rg.realigned." + vcfType + ".annovar.vcf.hg19_multianno.vcf","r") as f:
                readerList = list(csv.reader(f, delimiter='\t'))
                start = False
                # needs to be cleaned up
                for row in readerList:
                    if start:
                        data = row[9].split(':')
                        info = row[7].split(';')
                        NR = int(data[vcfDict[vcfType]['NR']])
                        NV = int(data[vcfDict[vcfType]['NV']])
                        isExonic = getValue(info, "ExonicFunc.refGene=")

                        try:
                            vaf = [NV/NR]
                        except ZeroDivisionError:
                            vaf = [-1]

                        newTable.append(row + vaf + isExonic)

                    elif row[0] == '#CHROM':
                        start = True
                        heading = row + ['vaf'] + ['isExonic']

            columns = {
                'vaf': initialHeadingSize,
                'isExonic': initialHeadingSize + 1
            }

            incFilters = [(columns['isExonic'],[".",'exonic'])]
            excFilters = []
            vaf = [0.02,0.4]


            incFiltered = filter(inclusionItterator, newTable)
            # depthFiltered = filter(lambda x: int(x[19]) >= depth, incFiltered)
            vafFiltered = filter(lambda x: float(x[columns['vaf']]) >= vaf[0] and float(x[columns['vaf']]) <= vaf[1], incFiltered)
            fullFiltered = list(filter(exclusionItterator, vafFiltered))

            # vafFiltered = filter(lambda x: float(x[9]) >= vaf[0] and float(x[9]) <= vaf[1], readerList)

            with open("../data/vcf/filtered/" + patient + ".sorted.rg.realigned." + vcfType + ".annovar.vcf.hg19_multianno-filtered.txt","w") as f:
                writer = csv.writer(f, delimiter ="\t")
                writer.writerow(heading)
                for row in fullFiltered:
                    writer.writerow(row)
            print(initialHeadingSize)
        except IOError:
            print('No file for ' + patient + ' ' + vcfType)

