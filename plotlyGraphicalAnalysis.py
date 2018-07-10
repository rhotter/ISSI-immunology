import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import csv

totalSick = 0
totalHealthy = 0

with open('../data/mutationCounts.csv') as csvfile:
    readCSV = csv.reader(csvfile)

    for row in readCSV:
        if (row[0]) == "Healthy":
            totalHealthy += int(row[2])

        if(row[0]) != "Healthy":
            totalSick += int(row[2])

trace = go.Bar(x=["Healthy", "Sick"], y= [totalHealthy, totalSick])
data = [trace]
layout = go.Layout(title='Healthy vs. Sick Patients', width=800, height=640)
fig = go.Figure(data=data, layout=layout)

py.image.save_as(fig, filename='data/HealthyVsSick.png')

from IPython.display import Image
Image('Healthy vs. Sick.png')
