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

mapbox_access_token = 'pk.eyJ1IjoiZ2FicmllbG1wYXVsYSIsImEiOiJjanRkMnRtMm0xMzZhNDRucjJtb3gwcjFkIn0.6MJfIbMZpOwezL8ccleUCQ'

all_data = dataframe.load_data()

init_lat = 22
init_lon = 79 
init_zoom = 4
marker_scale = 100000

data = [go.Scattermapbox(
        name = 'dataset',
        mode = 'markers'
        )]
    
layout = go.Layout(
    height = 1000,
    title = '<b>Indian population by city</b>',
    titlefont = {'family': 'Arial',
                    'size': 24},
    mapbox = go.layout.Mapbox(
        accesstoken = mapbox_access_token,
        bearing = 0,
        center = go.layout.mapbox.Center(
            lat = init_lat,
            lon = init_lon
        ),
        pitch = 0,
        zoom = init_zoom
))

layout = go.Layout(
height = 800,
title = '<b>Indian population by city</b>',
titlefont = {'family': 'Arial',
                'size': 24},
autosize = True,
hovermode = 'closest',
mapbox = go.layout.Mapbox(
    accesstoken = mapbox_access_token,
    bearing = 0,
    center = go.layout.mapbox.Center(
        lat = init_lat,
        lon = init_lon
    ),
    pitch = 0,
    zoom = init_zoom
))

updatemenus=list([dict(
    buttons=list([   
        dict(
            args=[{'visible': [True, False, False, False]}],
            label='Loke late truck',
            method='update'
        ),
        dict(
            args=[{'visible': [False, True, False, False]}],
            label='Placement issue',
            method='update'
        ),
        dict(
            args=[{'visible': [False, False, True, False]}],
            label='Yes compliance',
            method='update'
        ),
        dict(
            args=[{'visible': [False, False, False, True]}],
            label='Invalid trailer',
            method='update'
        )          
        ]),
    direction = 'down',
    pad = {'r': 10, 't': 10},
    showactive = True,
    x = 0.1,
    xanchor = 'left',
    y = 1.1,
    yanchor = 'top' 
)])

layout['updatemenus'] = updatemenus

fig = go.Figure(data=data, layout=layout) 

app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        dcc.Graph(id='live-update-map', figure=fig),
        dcc.Interval(
            id='interval-component',
            interval=5*60*1000,
            n_intervals=0
        ),
    ])
)


@app.callback(Output('live-update-map', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_map(n):

    for data_file in all_data:
        data.append(
            go.Scattermapbox(
            lon = data_file['lon'],
            lat = data_file['lat'],
            text = data_file['name'] + '- População ' + data_file['pop'].astype(str),
            mode = 'markers',
            visible = False,
            marker = go.scattermapbox.Marker(
                size = data_file['pop']/marker_scale,
                colorscale = 'Portland',
                color = data_file['pop'],
                showscale = True)
            )
        )
    
    layout = go.Layout(
    height = 1000,
    title = '<b>Indian population by city</b>',
    titlefont = {'family': 'Arial',
                    'size': 24},
    autosize = True,
    hovermode = 'closest',
    mapbox = go.layout.Mapbox(
        accesstoken = mapbox_access_token,
        bearing = 0,
        center = go.layout.mapbox.Center(
            lat = init_lat,
            lon = init_lon
        ),
        pitch = 0,
        zoom = init_zoom
    ))

    updatemenus=list([dict(
        buttons=list([   
            dict(
                args=[{'visible': [True, False, False, False]}],
                label='Loke late truck',
                method='update'
            ),
            dict(
                args=[{'visible': [False, True, False, False]}],
                label='Placement issue',
                method='update'
            ),
            dict(
                args=[{'visible': [False, False, True, False]}],
                label='Yes compliance',
                method='update'
            ),
            dict(
                args=[{'visible': [False, False, False, True]}],
                label='Invalid trailer',
                method='update'
            )          
            ]),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        x = 0.1,
        xanchor = 'left',
        y = 1.1,
        yanchor = 'top' 
    )])

    layout['updatemenus'] = updatemenus
    
    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)