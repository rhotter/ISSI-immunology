import plotly.plotly as py
import plotly.graph_objs as go

trace0 = go.Scatter(
    x=[1, 1.75, 2.5],
    y=[1, 1, 1],
    text=['$Sick$', '$Shared$', '$Healthy$'],
    mode='text',
    textfont=dict(
        color='black',
        size=18,
        family='Arial',
    )
)

data = [trace0]

layout = {
    'xaxis': {
        'showticklabels': False,
        'showgrid': False,
        'zeroline': False,
    },
    'yaxis': {
        'showticklabels': False,
        'showgrid': False,
        'zeroline': False,
    },
    'shapes': [
        {
            'opacity': 0.3,
            'xref': 'x',
            'yref': 'y',
            'fillcolor': 'blue',
            'x0': 0,
            'y0': 0,
            'x1': 2,
            'y1': 2,
            'type': 'circle',
            'line': {
                'color': 'blue',
            },
        },
        {
            'opacity': 0.3,
            'xref': 'x',
            'yref': 'y',
            'fillcolor': 'gray',
            'x0': 1.5,
            'y0': 0,
            'x1': 3.5,
            'y1': 2,
            'type': 'circle',
            'line': {
                'color': 'gray',
            },
        }
    ],
    'margin': {
        'l': 20,
        'r': 20,
        'b': 200
    },
    'height': 600,
    'width': 800,
}
fig = {
    'data': data,
    'layout': layout,
}
fig = go.Figure(data=data, layout=layout)

py.image.save_as(fig, filename='../data/mutComparisonChart.png')

from IPython.display import Image
Image('mutComparisonChart.png')
