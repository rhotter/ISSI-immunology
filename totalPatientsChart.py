import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt
import csv

totalSick = 0
totalHealthy = 0

with open("../data/mutationCountsNSR6.txt", "r") as f:
    readCSV = list(csv.reader(f, delimiter='\t'))
    for row in readCSV:
        if (row[0]) == "Healthy":
            totalHealthy += int(row[2])

        if(row[0]) != "Healthy":
            totalSick += int(row[2])

trace = go.Bar(x=["Healthy", "Sick"], y= [totalHealthy, totalSick])
data = [trace]
layout = go.Layout(
title='Total Patients Healthy vs. Sick',
xaxis=dict(
    title='',
    titlefont=dict(
        family='Courier New, monospace',
        size=18,
        color='#7f7f7f'
    )
),
yaxis=dict(
    title='Total Patients',
    titlefont=dict(
        family='Courier New, monospace',
        size=18,
        color='#7f7f7f'
    )
)
)
fig = go.Figure(data=data, layout=layout)

py.image.save_as(fig, filename='../data/HealthyVsSickNSR6.png')

from IPython.display import Image
Image('Healthy vs. Sick.png')
