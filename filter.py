"""
4 Jul. 2018

ISSI, team Noa Chapal

"""

import csv

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

def chi_squared(a,b,c,d):
    (a*d-b*c)**2 * (a+b+c+d)/((a+b)*(c+d)*(b+d)*(a+c))

# takes tab separated txt file as input and stores filtered rows in array
with open("total.txt","r") as f:

    readerList = list(csv.reader(f, delimiter='\t'))

    # runs the inclusion filter and then applies exclusion filter

    incFiltered = filter(inclusionItterator, readerList[1:])
    fullFiltered = filter(exclusionItterator, incFiltered)

    headings = readerList[0]

# writes txt file that only contains filters
with open("filteredTotal.txt", "w") as f:
    writer = csv.writer(f, delimiter ="\t")
    writer.writerow(headings)
    for row in fullFiltered:
        writer.writerow(row)

# Filtering frequency files by chi-squared
with open("smMIP_Old_P7_index17_S17.sorted.rg.realigned.freq.paired.Q30.txt") as f:
    readerList = list(csv.reader(f, delimiter='\t'))
    # runs the inclusion filter and then applies exclusion filter
    filtered = filter(______, readerList[1:])

    headings = readerList[0]
