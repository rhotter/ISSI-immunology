"""
5 Jul. 2018

ISSI, team Noa Chapal

"""

import csv

# list of inclusion and exclusion filters by column and value
incFilters = [(0,["smMIP_Old_P7_index17_S17"]), (6,["exonic"])]
excFilters = []

# array that stores the positions for the filtered total file
totalPositions = []


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


# takes tab separated txt file as input and stores filtered rows in array
with open("../data/total.txt","r") as f:

    readerList = list(csv.reader(f, delimiter='\t'))

    #runs the inclusion filter (without headings) and then applies exclusion filter


    incFiltered = filter(inclusionItterator, readerList[1:])
    fullFiltered = filter(exclusionItterator, incFiltered)

    #applies column headings

    headings = readerList[0]

# writes txt file that only contains filtered rows
with open("../data/filteredTotal.txt", "w") as f:
    writer = csv.writer(f, delimiter ="\t")
    writer.writerow(headings)
    for row in fullFiltered:
        writer.writerow(row)
        totalPositions.append(row[2])

# reads frequency file and filters out the rows that correspond to positions in the total file
with open("../data/smMIP_Old_P7_index17_S17.sorted.rg.realigned.freq.paired.Q30.txt","r") as f:
    next(f)
    readerList = list(csv.reader(f, delimiter='\t'))
    posFiltered = filter(lambda x:x[1] in totalPositions, readerList)

# writes a filtered frequency file that only contains filtered positions
with open("../data/filteredFrequency.txt","w") as f:
    writer = csv.writer(f, delimiter="\t")
    for row in posFiltered:
        writer.writerow(row)



