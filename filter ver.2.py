"""
5 Jul. 2018

ISSI, team Noa Chapal

"""

import csv

# list of inclusion and exclusion filters by column and value
incFilters = [(0,["smMIP_Old_P7_index8_S8", "smMIP_Old_P7_index17_S17", "smMIP_P7_index20_S34","smMIP_P7_index32_S46" ]), (6,["exonic"])]
excFilters = []

#stores set of positions for each index
patientsPositions = []
#array of current set of positions that will be pushed to patientsPositions
patientPositions = []


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
    previousRow = " "
    firstItt = True

    for row in fullFiltered:
        writer.writerow(row)

        # stores the index in first element of array for each position set
        patientTitle = row[0]

        if firstItt == True:
            patientPositions.append(patientTitle)
            firstItt = False

        # creates new array whenever there is a change in index
        if row[0] == previousRow or previousRow == " ":
            patientPositions.append(row[2])
        else:
            patientsPositions.append(patientPositions)
            patientPositions = []
            patientPositions.append(patientTitle)
            patientPositions.append(row[2])

        previousRow = row[0]

    #push the current set of positions to an ordered array by index
    patientsPositions.append(patientPositions)
    patientPositions = []

# reads frequency file for each index and filters out the rows
# that correspond to positions in the filtered total file
for i in patientsPositions:
    with open("../data/frequencyFiles/" + i[0] + ".sorted.rg.realigned.freq.paired.Q30.txt","r") as f:
        next(f)
        readerList = list(csv.reader(f, delimiter='\t'))
        posFiltered = filter(lambda x:x[1] in i[1:], readerList)

    with open("../data/frequencyFiles/filtered/"+ i[0] +"-filtered.txt","w") as f:
        writer = csv.writer(f, delimiter="\t")
        for row in posFiltered:
            writer.writerow(row)

