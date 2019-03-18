import dash
import pandas as pd
import plotly.graph_objs as go
import requests
import io
import numpy as np
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
from utils import dataframe

df = dataframe.load_data()

data = [go.Scattergeo()]

layout = go.Layout(
    height = 800,
    title = '<b>Indian population by city</b>',
    titlefont = {'family': 'Arial',
                    'size': 24},
    geo =  {'scope': 'asia',
            'projection': go.layout.geo.Projection(type = 'equirectangular'),
            'lonaxis': go.layout.geo.Lonaxis(range = [67.0, 91.0]),
            'lataxis': go.layout.geo.Lataxis(range = [5.0, 36.0]),
            'showland': True,
            'landcolor': '#f6e3db',
            'showlakes': True,
            'lakecolor': '#3498db',
            'subunitwidth': 1,
            'subunitcolor': "rgb(255, 255, 255)"},
    uirevision = True)

updatemenus=list([
    dict(
        buttons=list([   
            dict(
                args=['type', 'surface'],
                label='3D Surface',
                method='restyle'
            ),
            dict(
                args=['type', 'heatmap'],
                label='Heatmap',
                method='restyle'
            )             
        ]),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        x = 0.1,
        xanchor = 'left',
        y = 1.1,
        yanchor = 'top' 
    ),
])

layout['updatemenus'] = updatemenus

fig = go.Figure(data=data, layout=layout) 

app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        dcc.Graph(id='live-update-map', figure=fig),
        dcc.Interval(
            id='interval-component',
            interval=30*1000,
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-map', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_map(n):

    cities = df.shape[0]
    n_cities = cities
    sample = np.random.choice(cities, size=n_cities, replace=False)
    df_sample = df.iloc[sorted(sample)]

    data = [go.Scattergeo(
        name = 'dataset',
        lon = df_sample['lon'],
        lat = df_sample['lat'],
        text = df_sample['name'] + '- População ' + df_sample['pop'].astype(str),
        marker = dict(
            size = df_sample['pop']/10000,
            colorscale = 'Portland',
            color = df_sample['pop'],
            colorbar=dict(
                title="Incoming flightsFebruary 2011"
            ),
            line = {'width':0.5,
                    'color': '#2c3e50'},
            sizemode = 'area'))]
    
    layout = go.Layout(
        height = 800,
        title = '<b>Indian population by city</b>',
        titlefont = {'family': 'Arial',
                     'size': 24},
        geo =  {'scope': 'asia',
                'projection': go.layout.geo.Projection(type = 'equirectangular'),
                'lonaxis': go.layout.geo.Lonaxis(range = [67.0, 91.0]),
                'lataxis': go.layout.geo.Lataxis(range = [5.0, 36.0]),
                'showland': True,
                'landcolor': '#f6e3db',
                'showlakes': True,
                'lakecolor': '#3498db',
                'subunitwidth': 1,
                'subunitcolor': "rgb(255, 255, 255)"},
        uirevision = True)    
    
    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)