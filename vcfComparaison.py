import csv
patient = "smMIP_Old_P7_index17_S17"

firstSample = []
secondSample = []
commonSample = []

with open("../data/vcf/filtered/" + patient + ".sorted.rg.realigned.platypus.annovar.vcf.hg19_multianno-filtered.txt", "r") as f:
    readerList = list(csv.reader(f, delimiter='\t'))
    headings = readerList[0]
    for row in readerList[1:]:
        firstSample.append(row)

with open("../data/vcf/filtered/" + patient + ".sorted.rg.realigned.varscan.annovar.vcf.hg19_multianno-filtered.txt","r") as f:
    next(f)
    readerList = list(csv.reader(f, delimiter='\t'))
    for row in readerList:
        secondSample.append(row)

for r in firstSample:
    for s in secondSample:
        if r[0:2] == s[0:2]:
            commonSample.append(s)

with open("../data/vcf/filtered/commons/" + patient + ".sorted.rg.realigned.compared.annovar.vcf.hg19_multianno-filtered.txt","w") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(headings)
    for row in commonSample:
        writer.writerow(row)

print(commonSample)