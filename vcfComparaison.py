import csv

with open("../data/vcf/" + patient + ".sorted.rg.realigned." + vcfType + ".annovar.vcf.hg19_multianno.vcf", "r") as f:
    readerList = list(csv.reader(f, delimiter='\t'))