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
marker_scale = 50000

data = [go.Scattermapbox(
        name = 'dataset',
        mode = 'markers'
        )]

layout = go.Layout(
height = 840,
margin = dict(t=30),
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

fig = go.Figure(data=data, layout=layout) 

app = dash.Dash(__name__)
app.layout = html.Div( children = [
    
    html.H1('Indian population by city', style = {'textAlign': 'Center', 'margin-left': '4%'}),
    
    html.Div([
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': 'Loke late truck', 'value': 0},
                    {'label': 'Placement issue', 'value': 1},
                    {'label': 'Yes compliance', 'value': 2},            
                    {'label': 'Invalid trailer', 'value': 3}
                    ]
                ),
            ],
            style = {
                'display': 'inline-block',
                'width': '10%',
                'margin-left': '46%',
            }
    ),  

    html.Div([      
        dcc.Graph(
            id = 'live-update-map',
            figure = fig,
            config = dict(
                scrollWheel = True),
            ),
        ]
    ),

    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,
        n_intervals=0
    )
])


@app.callback(Output('live-update-map', 'figure'),
              [Input('interval-component', 'n_intervals'), Input('dropdown', 'value')])
def update_map(n, value):

    if value == None:
        data = [go.Scattermapbox(
        name = 'dataset',
        mode = 'markers'
        )]

    else:
        data =  [go.Scattermapbox(
            lon = all_data[value]['lon'],
            lat = all_data[value]['lat'],
            text = all_data[value]['name'] + '- População ' + all_data[value]['pop'].astype(str),
            mode = 'markers',
            marker = go.scattermapbox.Marker(
                # size = all_data[value]['pop']/marker_scale,
                size = 15,
                colorscale = 'Portland',
                color = all_data[value]['pop'],
                showscale = False)
        )]

    layout = go.Layout(
        height = 840,
        margin = dict(t=30),
        autosize = True,
        hovermode = 'closest',
        uirevision = 'dataset',
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
    
    fig = go.Figure(data=data,layout=layout)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)