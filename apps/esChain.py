#------------------------------------
# Import Modules                    #
#------------------------------------
import json
import base64
import datetime
import requests
import pathlib
import math
import pandas as pd
import flask
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from plotly import tools
from app import app
#------------------------------------
# Data Paths                        #
#------------------------------------
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
# Futures Data
es_data = pd.read_csv(DATA_PATH.joinpath("ES.csv"))
# Options Chain Data
filename2 = ('Live Options Chain.csv')
data2 = pd.read_csv(DATA_PATH.joinpath(filename2))
#------------------------------------
# Show most recent strikes
df2 = data2[-20:]
vega_l = []
for x_ in df2['Put Vega']:
	vega_l.append("{:.3f}".format(x_))
df2['Put Vega'] = df2['Put Vega'].map('{:.3f}'.format)
df2['Put Gamma'] = df2['Put Gamma'].map('{:.3f}'.format)
df2['Call Vega'] = df2['Call Vega'].map('{:.3f}'.format)
df2['Call Gamma'] = df2['Call Gamma'].map('{:.3f}'.format)
df2['Put Theta'] = df2['Put Theta'].map('{:.3f}'.format)
df2['Call Theta'] = df2['Call Theta'].map('{:.3f}'.format)
#------------------------------------
def fetchData():
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    filename2 = ('Live Options Chain.csv')
    data2 = pd.read_csv(DATA_PATH.joinpath(filename2))
    #------------------------------------
    # Show most recent strikes
    df2 = data2[-20:]
    vega_l = []
    for x_ in df2['Put Vega']:
    	vega_l.append("{:.3f}".format(x_))
    df2['Put Vega'] = df2['Put Vega'].map('{:.3f}'.format)
    df2['Put Gamma'] = df2['Put Gamma'].map('{:.3f}'.format)
    df2['Call Vega'] = df2['Call Vega'].map('{:.3f}'.format)
    df2['Call Gamma'] = df2['Call Gamma'].map('{:.3f}'.format)
    df2['Put Theta'] = df2['Put Theta'].map('{:.3f}'.format)
    df2['Call Theta'] = df2['Call Theta'].map('{:.3f}'.format)
    return df2
#------------------------------------
# Styles
styles = []
styles.append({
            'if': {'row_index': 'odd'},
            'backgroundColor': '#1D262F'
        })
styles.append({
            'if': {'row_index': 'even'},
            'backgroundColor': '#242E3F'
        }) 
styles.append({
            'color': 'white'
        })
def call_Vol(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ] 
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        #color = 'white' if i > len(bounds) / 2. else 'black'
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(-90deg,
                    #810f7c 0%,
                    #810f7c {max_bound_percentage}%,
                    #242E3F {max_bound_percentage}%,
                    #242E3F 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'color': 'white',
            'paddingBottom': 2,
            'paddingTop': 2,
        })
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column,
                'row_index': 'odd'
            },
            'background': (
                """
                    linear-gradient(270deg,
                    #810f7c 0%,
                    #810f7c {max_bound_percentage}%,
                    #1D262F {max_bound_percentage}%,
                    #1D262F 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'color': 'white',
            'paddingBottom': 2,
            'paddingTop': 2
        })
        
def put_Vol(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        #color = 'white' if i > len(bounds) / 2. else 'black'
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column

            },
            'background': (
                """
                    linear-gradient(90deg,
                    #810f7c 0%,
                    #810f7c {max_bound_percentage}%,
                    #242E3F {max_bound_percentage}%,
                    #242E3F 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'color': 'white',
            'paddingBottom': 2,
            'paddingTop': 2
        })
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column,
                'row_index': 'odd'
            },
            'background': (
                """
                    linear-gradient(90deg,
                    #810f7c 0%,
                    #810f7c {max_bound_percentage}%,
                    #1D262F {max_bound_percentage}%,
                    #1D262F 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'color': 'white',
            'paddingBottom': 2,
            'paddingTop': 2
        })
def call_OI(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        #color = 'white' if i > len(bounds) / 2. else 'black'
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(90deg,
                    #810f7c 0%,
                    #810f7c {max_bound_percentage}%,
                    #242E3F {max_bound_percentage}%,
                    #242E3F 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'color': 'white',
            'paddingBottom': 2,
            'paddingTop': 2
        })
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column,
                'row_index': 'odd'
            },
            'background': (
                """
                    linear-gradient(90deg,
                    #810f7c 0%,
                    #810f7c {max_bound_percentage}%,
                    #1D262F {max_bound_percentage}%,
                    #1D262F 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'color': 'white',
            'paddingBottom': 2,
            'paddingTop': 2
        })
def put_OI(df, column):
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [
        ((df[column].max() - df[column].min()) * i) + df[column].min()
        for i in bounds
    ]
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        #color = 'white' if i > len(bounds) / 2. else 'black'
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column
            },
            'background': (
                """
                    linear-gradient(-90deg,
                    #810f7c 0%,
                    #810f7c {max_bound_percentage}%,
                    #242E3F {max_bound_percentage}%,
                    #242E3F 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            
            'color': 'white',

            'paddingBottom': 2,
            'paddingTop': 2,
        })
        styles.append({
            'if': {
                'filter_query': (
                    '{{{column}}} >= {min_bound}' +
                    (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                'column_id': column,
                'row_index': 'odd'
            },
            'background': (
                """
                    linear-gradient(270deg,
                    #810f7c 0%,
                    #810f7c {max_bound_percentage}%,
                    #1D262F {max_bound_percentage}%,
                    #1D262F 100%)
                """.format(max_bound_percentage=max_bound_percentage)
            ),
            'color': 'white',
            'paddingBottom': 2,
            'paddingTop': 2
        })


def greeks_(df2, n_bins=5, columns='all'):
    import colorlover
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df2:
            df2_numeric_columns = df2.select_dtypes('number').drop(['id'], axis=1)
        else:
            df2_numeric_columns = df2.select_dtypes('number')
    else:
        df2_numeric_columns = df2[columns]
    df2_max = df2_numeric_columns.max().max()
    df2_min = df2_numeric_columns.min().min()
    ranges = [
        ((df2_max - df2_min) * i) + df2_min
        for i in bounds
    ]
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colorlover.scales[str(n_bins)]['seq']['BuPu'][i - 1]
        color = 'white' if i > len(bounds) / 2. else 'black'
        for column in df2_numeric_columns:
            styles.append(
            {
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
        	'backgroundColor': backgroundColor,
                'color': color
                }) 
#------------------------------------
call_OI(df2,'Call Open Interest')
put_OI(df2, 'Put Open Interest')
call_Vol(df2, 'Call Volume')
put_Vol(df2, 'Put Volume')
greeks_(df2, columns=['Put Vega'])
greeks_(df2, columns=['Call Vega'])
greeks_(df2, columns=['Put Gamma'])
greeks_(df2, columns=['Call Gamma'])
greeks_(df2, columns=['Put Delta'])
greeks_(df2, columns=['Call Delta'])
styles.append({'if': {'column_id': 'Strike'},
            'backgroundColor': '#edf8fb',
            'color': 'black'})
styles.append({
            'if': {'column_id': 'Call Open Interest',
            	   'filter_query': '{{Call Open Interest}} = {}'.format(df2['Call Open Interest'].max())
            	  },
            	  'color': 'yellow'
        })
styles.append({
            'if': {'column_id': 'Call Volume',
            	   'filter_query': '{{Call Volume}} = {}'.format(df2['Call Volume'].max())
            	  },
            	  'color': 'yellow'
        })
styles.append({
            'if': {'column_id': 'Put Volume',
            	   'filter_query': '{{Put Volume}} = {}'.format(df2['Put Volume'].max())
            	  },
            	  'color': 'yellow'
        })
styles.append({
            'if': {'column_id': 'Put Open Interest',
            	   'filter_query': '{{Put Open Interest}} = {}'.format(df2['Put Open Interest'].max())
            	  },
            	  'color': 'yellow'
        })
#------------------------------------
# Graph                             #
#------------------------------------
fig = px.area(es_data,x='Date',y='Bid',color_discrete_sequence=['#810f7c'])
fig["layout"][
    "uirevision"
] = "The User is always right"  # Ensures zoom on graph is the same on update
fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
fig["layout"]["xaxis"]["tickformat"] = "%H:%M"
fig["layout"]["yaxis"]["range"] = [min(es_data['Bid']),max(es_data['Bid'])]
fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
fig["layout"]["autosize"] = True
fig["layout"]["height"] = 630
#fig["layout"]["yaxis"]["gridwidth"] = 1
fig["layout"]["yaxis"]["title"] = 'Price'
fig["layout"]["xaxis"]["title"] = ''
fig["layout"].update(paper_bgcolor="#1D262F", plot_bgcolor="#1D262F")
#------------------------------------
# News Api                          #
#------------------------------------

# API Requests for news div
news_requests = requests.get(
    "https://newsapi.org/v2/top-headlines?sources=bloomberg&apiKey=ef2168f74e6c4824a1ff4db29eb25b07"
)
# API Call to update news
def update_news():
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url"]])
    max_rows = 10
    return html.Div(
        children=[
            html.P(className="p-news", children="Headlines"),
            html.P(
                className="p-news float-right",
                children="Last update : "
                + datetime.datetime.now().strftime("%H:%M:%S"),
            ),
            html.Table(
                className="table-news",
                children=[
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    html.A(
                                        className="td-link",
                                        children=df.iloc[i]["title"],
                                        href=df.iloc[i]["url"],
                                        target="_blank",
                                    )
                                ]
                            )
                        ]
                    )
                    for i in range(min(len(df), max_rows))
                ],
            ),
        ]
    )
#------------------------------------
# Layout                            #
#------------------------------------

# Dash App Layout
layout = html.Div(
    className="row",
    children=[
        # Left Panel Div
        html.Div(
            className="three columns div-left-panel",
            children=[
                # Div for Left Panel App Info
                html.Div(
                    className="div-info",
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("dash-logo-new.jpg")
                        ),
                        html.H6(className="title-header", children="QG Terminal")
                    ],
                ),
                # Div for News Headlines
                html.Div(
                    className="div-news",
                    children=[html.Div(id="news2", children=update_news())],
                ),
            ],
        ),
        # Top Nav Bar
        html.Div(
            className="nine columns div-right-panel",
            children=[
                # Nav Bar
                dbc.Navbar(className="cmdTest",children=
                [
                    dbc.Col(dbc.NavbarBrand("QG Terminal", href="#"), sm=3, md=2),
                    dbc.Col(dbc.Input(id="input2",type="search", 
                    placeholder="Enter Command...",debounce=True)),
                    html.P(id='output2'),
                ],
                color="#1D262F",
                dark=True,
                ),
            ],
        ),
        # Body
        html.Div(
            className = 'oChart',
            children = [
                dcc.Interval(
                    id="interval-component",
                    interval=65000,
                    n_intervals=0
                ),
                dcc.Graph(id="live-update-graph")
            ]
        ),
        # Options Chain Testing
        html.Div(className="oChain_",
                 children=[dcc.Interval(id='graph-update',interval=60000,n_intervals=0),
                           dash_table.DataTable(
                                   id='table',
                                   columns=[{"name": i, "id": i} for i in df2.columns],
                                   style_table = {'minHeight': '600px', 'height': '600px', 'maxHeight': '600px',
                                                  'minWidth': '900px', 'width': '900px', 'maxWidth': '900px',
                                                   'margin-left': '25px', 'margin-top': '-35px'},
                                   style_header ={'backgroundColor':'rgb(29, 38, 47)'},
                                   style_cell={'textAlign': 'center','border': '0.05px solid #5c8cbe'},
                                   data = [{}],
                                   style_data_conditional=styles,
                                   )
        ]),
        # Vega Held Chart
        html.Div(
            className = 'vChart',
            children = [
                dcc.Interval(
                    id="interval-component",
                    interval=65000,
                    n_intervals=0
                ),
                dcc.Graph(id="live-update-graph3")
            ]
        ),
        # Option Flow Chart
        html.Div(
            className = 'ofChart',
            children = [
                dcc.Interval(
                    id="interval-component",
                    interval=65000,
                    n_intervals=0
                ),
                dcc.Graph(id="live-update-graph4")
            ]
        ),
        # Gamma Held Chart
        html.Div(
            className = 'gChart',
            children = [
                dcc.Interval(
                    id="interval-component",
                    interval=65000,
                    n_intervals=0
                ),
                dcc.Graph(id="live-update-graph2")
            ]
        ),
    ])
#------------------------------------
# Dynamic Callbacks                 #
#------------------------------------
# Callback to update option flow graph
@app.callback(Output('live-update-graph4', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    # Loading historical tick data
    vOI_data = pd.read_csv(DATA_PATH.joinpath("oFlow.csv"))
    fig = px.bar(vOI_data,x='Strike',y='Volume',color='Type',color_discrete_sequence=['#5c8cbe','#810f7c'])
    #fig.update_traces(texttemplate='%{text:.2s}', textposition='inside',textfont=dict(color="#fff"))
    #fig.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
    fig["layout"][
        "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on updat
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    fig["layout"]["yaxis"]["range"] = [min(vOI_data['Volume']),max(vOI_data['Volume'])*1.15]
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 400
    fig["layout"]["width"] = 600
    #fig["layout"]["yaxis"]["gridcolor"] = "#3E3F40"
    fig["layout"]["yaxis"]["gridwidth"] = 1
    fig["layout"]["yaxis"]["title"] = 'Volume (24 hrs)'
    fig["layout"]["xaxis"]["title"] = 'Strike'
    fig["layout"]["yaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["xaxis"]["gridcolor"] = "#242E3F"
    fig.update_layout(legend=dict(font=dict(color="#87B4E5")))
    fig["layout"].update(paper_bgcolor="#1D262F", plot_bgcolor="#1D262F")
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_layout(title_text='Option Flow (Daily)',title_x=0.5,title_font_color='#87B4E5',
                yaxis=dict(color='#87B4E5'),xaxis=dict(color='#87B4E5'))
    return fig

# Callback to update Vega held graph
@app.callback(Output('live-update-graph3', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    # Loading historical tick data
    vOI_data = pd.read_csv(DATA_PATH.joinpath("VegaOI.csv"))
    fig = px.area(vOI_data,x='Strike',y='Vega OI',color_discrete_sequence=['#810f7c'])
    fig["layout"][
        "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on updat
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    fig["layout"]["yaxis"]["range"] = [min(vOI_data['Vega OI']),max(vOI_data['Vega OI'])]
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 400
    fig["layout"]["width"] = 600
    fig.update_layout(title_text='Vega Open Interest', title_x=0.5)
    #fig["layout"]["yaxis"]["gridcolor"] = "#3E3F40"
    fig["layout"]["yaxis"]["gridwidth"] = 1
    fig["layout"]["yaxis"]["title"] = 'Vega'
    fig["layout"]["xaxis"]["title"] = 'Strike'
    fig["layout"]["yaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["xaxis"]["gridcolor"] = "#242E3F"
    fig["layout"].update(paper_bgcolor="#1D262F", plot_bgcolor="#1D262F")
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_layout(title_text='Vega (Call vs Put) Ratio',title_x=0.5,title_font_color='#87B4E5',
                yaxis=dict(color='#87B4E5'),xaxis=dict(color='#87B4E5'))
    return fig

# Callback to update Gamma held graph
@app.callback(Output('live-update-graph2', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    #-------------------------------------------------------------------------------------------------------------------------------
    # Data
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    gOI_data = pd.read_csv(DATA_PATH.joinpath("GammaOI.csv"))
    #-------------------------------------------------------------------------------------------------------------------------------
    # Creating figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=gOI_data['Strike'],y=gOI_data['Call Gamma OI'],fill='tozeroy',line_color='#5c8cbe',name="Call"))
    fig.add_trace(go.Scatter(x=gOI_data['Strike'],y=gOI_data['Put Gamma OI'],fill='tozeroy',line_color='#810f7c',name="Put"))
    fig["layout"][
        "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on updat
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    #-------------------------------------------------------------------------------------------------------------------------------
    # conditional statement to scale y-axis by largest
    if max(gOI_data['Call Gamma OI']) > max(gOI_data['Put Gamma OI']):
    	fig["layout"]["yaxis"]["range"] = [min(gOI_data['Call Gamma OI']),max(gOI_data['Call Gamma OI'])]
    else:
    	fig["layout"]["yaxis"]["range"] = [min(gOI_data['Put Gamma OI']),max(gOI_data['Put Gamma OI'])]
    #-------------------------------------------------------------------------------------------------------------------------------
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 400
    fig["layout"]["width"] = 600
    fig.update_layout(title_text='Gamma Open Interest', title_x=0.5)
    #fig["layout"]["yaxis"]["gridcolor"] = "#3E3F40"
    fig["layout"]["yaxis"]["gridwidth"] = 1
    fig["layout"]["yaxis"]["title"] = 'Gamma'
    fig["layout"]["xaxis"]["title"] = 'Strike'
    fig["layout"]["yaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["xaxis"]["gridcolor"] = "#242E3F"
    fig.update_layout(legend=dict(font=dict(color="#87B4E5")))
    fig["layout"].update(paper_bgcolor="#1D262F", plot_bgcolor="#1D262F")
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_layout(title_text='Gamma Open Interest',title_x=0.5,title_font_color='#87B4E5',
                yaxis=dict(color='#87B4E5'),xaxis=dict(color='#87B4E5'))
    return fig
# Callback to update Last Price Graph
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    # Loading historical tick data
    es_data = pd.read_csv(DATA_PATH.joinpath("ES.csv"))
    fig = px.area(es_data,x='Date',y='Last Price',color_discrete_sequence=['#810f7c'])
    fig["layout"][
        "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on updat
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    fig["layout"]["xaxis"]["tickformat"] = "%H:%M"
    fig["layout"]["yaxis"]["range"] = [min(es_data['Last Price']),max(es_data['Last Price'])*1.0001]
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 630
    fig["layout"]["yaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["xaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["yaxis"]["gridwidth"] = 1
    #fig["layout"]["xaxis"]["showgrid"]=False
    #fig["layout"]["yaxis"]["showgrid"]=False
    fig["layout"]["yaxis"]["title"] = 'Price'
    fig["layout"]["xaxis"]["title"] = ''
    fig["layout"].update(paper_bgcolor="#1D262F", plot_bgcolor="#1D262F")
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_layout(title_text='/ESH1 Last Price',title_x=0.5,title_font_color='#87B4E5',
                yaxis=dict(color='#87B4E5'),xaxis=dict(color='#87B4E5'))
    return fig

# CAllback function to update options chain
@app.callback(
     dash.dependencies.Output('table', 'data'),
    [dash.dependencies.Input('graph-update', 'n_intervals')])
def update_table(n):
    updated_data = fetchData()
    return updated_data.to_dict('records')

# Callback function to update command bar
@app.callback(Output("output2", "children"), [Input("input2", "value")])
def output_text(value):
    if value == "/oChain":
        return dcc.Location(id='test',pathname='/apps/oChain')
    if value == "/home":
        return dcc.Location(id='home__',pathname='/apps/home')
    if value == "/usRates":
        return dcc.Location(id="usRates",pathname='/apps/usRates')
    if value == "/portfolio":
        return dcc.Location(id="portfolio",pathname='/apps/portfolio')
    if value == "/soma":
    	return dcc.Location(id="soma",pathname='/apps/soma')
    if value == None:
        print('Enter Command in searchbar')
    else:
        print('incorrect command!')
    print(value)
    return value

# Callback to update live clock
@app.callback(Output("live_clock2", "children"), [Input("interval", "n_intervals")])
def update_time(n):
    return datetime.datetime.now().strftime("%H:%M:%S")

# Callback to update news
@app.callback(Output("news2", "children"), [Input("i_news", "n_intervals")])
def update_news_div(n):
    return update_news()
#------------------------------------
