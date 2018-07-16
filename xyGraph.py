
import sklearn
import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np
from sklearn import datasets, linear_model

# Load the diabetes dataset
diabetes = datasets.load_diabetes()


# Use only one feature
diabetes_X = diabetes.data[:, np.newaxis, 2]

# Split the data into training/testing sets
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]

# Split the targets into training/testing sets
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test = diabetes.target[-20:]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)

def data_to_plotly(x):
    k = []

    for i in range(0, len(x)):
        k.append(x[i][0])

    return k

p1 = go.Scatter(x=data_to_plotly(diabetes_X_test),
                y=diabetes_y_test,
                mode='markers',
                marker=dict(color='green')
               )

p2 = go.Scatter(x=data_to_plotly(diabetes_X_test),
                y=regr.predict(diabetes_X_test),
                mode='lines',
                line=dict(color='red', width=3)
                )

layout = go.Layout(xaxis=dict(ticks='', showticklabels=False,
                              zeroline=False),
                   yaxis=dict(ticks='', showticklabels=False,
                              zeroline=False),
                   showlegend=False, hovermode='closest')

fig = go.Figure(data=[p1, p2], layout=layout)

py.iplot(fig)

py.image.save_as(fig, filename='../data/ComparisonChart.png')

from IPython.display import Image
Image('ComparisonChart.png')
