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

# Data Route
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

#------------------------------------
# Asset Purchase Schedule Dataset   #
#------------------------------------
df_AP_S = pd.read_csv(DATA_PATH.joinpath('schedule.csv'))
df_AP_S = df_AP_S.replace('\n','',regex=True)
#df_AP_S.set_index('Date')
#------------------------------------
# Dates of the week
weekday_n = datetime.datetime.today().weekday()
today = datetime.datetime.today().strftime('%m/%d/%y').lstrip("0").replace("0",'')                                       # Today
if weekday_n == 0:                                                                                                       # If today is monday
    weekday1 = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Tuesday
    weekday2 = (datetime.datetime.today() + datetime.timedelta(days=2)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Wednesday 
    weekday3 = (datetime.datetime.today() + datetime.timedelta(days=3)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Thrusday
    weekday4 = (datetime.datetime.today() + datetime.timedelta(days=4)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Friday
    week_l = [today, weekday1,weekday2,weekday3,weekday4] # List of dates this week

if weekday_n == 1:                                                                                                       # If today is tuesday
    weekday1 = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Monday
    weekday2 = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Wednesday 
    weekday3 = (datetime.datetime.today() + datetime.timedelta(days=2)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Thrusday
    weekday4 = (datetime.datetime.today() + datetime.timedelta(days=3)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Friday
    week_l = [weekday1,today,weekday2,weekday3,weekday4] # List of dates this week

if weekday_n == 2:                                                                                                       # If today is wednesday
    weekday1 = (datetime.datetime.today() - datetime.timedelta(days=2)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Monday
    weekday2 = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Tuesday
    weekday3 = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Thrusday
    weekday4 = (datetime.datetime.today() + datetime.timedelta(days=2)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Friday
    week_l = [weekday1,weekday2,today,weekday3,weekday4] # List of dates this week
if weekday_n == 3:                                                                                                       # If today is thurday
    weekday1 = (datetime.datetime.today() - datetime.timedelta(days=3)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Monday
    weekday2 = (datetime.datetime.today() - datetime.timedelta(days=2)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Tuesday
    weekday3 = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Wednesday
    weekday4 = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Friday
    week_l = [weekday1,weekday2,weekday3,today,weekday4] # List of dates this week
if weekday_n == 4:                                                                                                       # If today is friday
    weekday1 = (datetime.datetime.today() - datetime.timedelta(days=4)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Monday
    weekday2 = (datetime.datetime.today() - datetime.timedelta(days=3)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Tuesday
    weekday3 = (datetime.datetime.today() - datetime.timedelta(days=2)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Wednesday
    weekday4 = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%m/%d/%y').lstrip("0").replace("0","") # Thursday
    week_l = [weekday1,weekday2,weekday3,weekday4,today] # List of dates this week
#------------------------------------
# Filter Dataset by Dates of the week
start_date = week_l[0]
#end_date = week_l[-1]
after_start = df_AP_S["Date"] >= start_date
#before_end = df_AP_S["Date"] <= end_date
#between = after_start & before_end
filtered_dataset = df_AP_S.loc[after_start]
#------------------------------------
# SOMA Dataset                      #
#------------------------------------
df_s = pd.read_csv(DATA_PATH.joinpath('SOMA.csv'))
styles_s = []
styles_s.append({
            'if': {'row_index': 'odd'},
            'backgroundColor': '#1D262F'
        })
styles_s.append({
            'if': {'row_index': 'even'},
            'backgroundColor': '#242E3F'
        }) 
styles_s.append({
            'color': 'white'
        })
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
            html.Div(className="p-news", children="Headlines"),
            html.Div(
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
                        html.H6(className="title-header", children="QG Terminal"),
                    ],
                ),
                # Div for News Headlines
                html.Div(
                    className="div-news",
                    children=[html.Div(className="news_",id="news4", children=update_news())],
                ),
            ],
        ),
        # Top Nav Bar
        html.Div(
            className="nine columns div-right-panel",
            children=[
                # Nav Bar
                dbc.Navbar(
                [
                    dbc.Col(dbc.NavbarBrand("QG Terminal", href="#"), sm=3, md=2),
                    dbc.Col(dbc.Input(id="input4",type="search", 
                    placeholder="Enter Command...",debounce=True)),
                    html.P(id='output4'),
                ],
                color="dark",
                dark=True,
                ),
            ],
        ),
        # Body

        # Soma Table
        #html.Div(
        #    className="SOMA", 
        #    children=
        #    [
        #        html.P(className='table_title',
        #               children=
        #               [
        #                   "SPortfolio"
        #               ]),
        #        dash_table.DataTable(
        #            id='Soma-Table',
        #            columns=[{"name": i,"id": i}for i in df_s.columns],
        #            data=df_s.to_dict('records'),
        #            style_data_conditional=styles_s,
        #            style_cell = {'textAlign': 'center','border': '0.05px solid #5c8cbe'},
        #            style_header={'backgroundColor':'#1D262F'}
        #        )
        #    ]
        #),

        # Asset Purchase Schedule Table
        html.Div(
            className="AP_Schedule",
            children = 
            [
                html.P(className="APS_Title",
                children = [
                    "As Purchase Schedule"
                ]),
                dash_table.DataTable(
                    id='AP-Schedule',
                    columns=[{"name": i,"id": i}for i in df_AP_S.columns],
                    data=df_AP_S.to_dict('records'),
                    style_data_conditional=styles_s,
                    style_cell = {'whitespace': 'normal','height': 'auto','textAlign': 'center','border': '0.05px solid #5c8cbe'},
                    #style_cell_conditional = [
                    #    {'if': {'column_id': 'Security'},
                    #    'width':'50%'},
                    #    #{'if': {'column_id': 'Max Purchase Size'},
                    #    #'width':'50%'},
                    #],
                    style_header={'backgroundColor':'#1D262F'}
                )
            ]
        ),

        # Soma bargraph
        html.Div(
            className = "soma_bargraph", 
            children = 
            [
                dcc.Interval(
                    id="interval-component",
                    interval=65000,
                    n_intervals = 0
                ),
                dcc.Graph(id="soma-bargraph")
            ]
        ),
        # Change Bargraph
        html.Div(
            className="Change_Graph",
            children=
            [
                dcc.Interval(
                    id="interval-component",
                    interval=65000,
                    n_intervals=0
                ),
                dcc.Graph(id="Change-Graph")
            ]
        ),

        # T-Notes & Bonds Area Graph
        html.Div(
            className="T-Notes_T-Bonds",
            children=
            [
                dcc.Interval(
                    id="interval-component",
                    interval=65000,
                    n_intervals = 0
                ),
                dcc.Graph(id="T_Notes_T_Bonds")
            ]
        ),

        # Total Area Graph
        html.Div(
            className="Total_Graph",
            children=
            [
                dcc.Interval(
                    id="interval-component",
                    interval=65000,
                    n_intervals = 0
                ),
                dcc.Graph(id="Total-Graph")
            ]
        ),

        # T Bills Area Graph
        html.Div(
            className="Bills_Graph",
            children =
            [
                dcc.Interval(
                    id="interval-component",
                    interval=65000,
                    n_intervals=0
                ),
                dcc.Graph(id="Bills-Graph")
            ]
        ),

        # TIPS Area Graph
        html.Div(
            className="Tips_Graph",
            children =
            [
                dcc.Interval(
                    id="interval-component",
                    interval = 65000,
                    n_intervals =0
                ),
                dcc.Graph(id="Tips-Graph")
            ]
        ),

        # Agency Mortgage-Backed Securities
        html.Div(
            className="AMBS_Graph",
            children=
            [
                dcc.Interval(
                    id="interval_component",
                    interval=65000,
                    n_intervals=0
                ),
                dcc.Graph(id="AMBS-Graph")
            ]
        ),
    ]
)
#------------------------------------
# Dynamic Callbacks                 #
#------------------------------------


# Callback for change bargraph
@app.callback(Output('Change-Graph','figure'),
            [Input('interval-component','n_intervals')])
def update_graph_live(n):
    # Import dataset
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    data_sc = pd.read_csv(DATA_PATH.joinpath("SOMA_hist.csv"))
    # Plotting
    fig = px.bar(data_sc,x='Date',y='Change',color_discrete_sequence=['#5c8cbe'])
    fig["layout"][
    "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on updat
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 400
    fig["layout"]["width"] = 500
    fig["layout"]["yaxis"]["gridwidth"] = 1
    fig["layout"]["yaxis"]["title"] = 'Value'
    fig["layout"]["xaxis"]["title"] = 'Date'
    fig["layout"]["yaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["xaxis"]["gridcolor"] = "#242E3F"
    fig["layout"].update(paper_bgcolor="#1D262F", plot_bgcolor="#1D262F")
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_layout(title_text='Change in SOMA Holdings (Weekly)',title_x=0.5,
    title_font_color='#87B4E5',yaxis=dict(color='#87B4E5'),xaxis=dict(color='#87B4E5'))
    return fig
# Callback for AMBS Graph
@app.callback(Output('AMBS-Graph','figure'),
             [Input('interval_component', 'n_intervals')])
def update_graph_live(n):
    # Import Dataset
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    data_sc = pd.read_csv(DATA_PATH.joinpath("SOMA_hist.csv"))
    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_sc['Date'],y=data_sc['AMBS'],fill='tozeroy',line_color='#810f7c'))
    fig["layout"][
    "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on update
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 400
    fig["layout"]["width"] = 450
    fig["layout"]["yaxis"]["gridwidth"] = 1
    fig["layout"]["yaxis"]["title"] = 'Value'
    fig["layout"]["xaxis"]["title"] = 'Date'
    fig["layout"]["yaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["xaxis"]["gridcolor"] = "#242E3F"
    fig["layout"].update(paper_bgcolor="#1D262F", plot_bgcolor="#1D262F")
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_layout(title_text='AMBS Holdings',title_x=0.5,
    title_font_color='#87B4E5',yaxis=dict(color='#87B4E5'),xaxis=dict(color='#87B4E5'))
    return fig


# Callback for Tips Graph
@app.callback(Output('Tips-Graph', 'figure'),
              [Input('interval-component','n_intervals')])
def update_graph_live(n):
    # Import Dataset
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    data_sc = pd.read_csv(DATA_PATH.joinpath("SOMA_hist.csv"))
    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_sc['Date'],y=data_sc['TIPS'],fill='tozeroy',line_color='#5c8cbe'))
    fig["layout"][
    "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on update
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 400
    fig["layout"]["width"] = 450
    fig["layout"]["yaxis"]["gridwidth"] = 1
    fig["layout"]["yaxis"]["title"] = 'Value'
    fig["layout"]["xaxis"]["title"] = 'Date'
    fig["layout"]["yaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["xaxis"]["gridcolor"] = "#242E3F"
    fig["layout"].update(paper_bgcolor="#1D262F", plot_bgcolor="#1D262F")
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_layout(title_text='TIPS Holdings',title_x=0.5,
    title_font_color='#87B4E5',yaxis=dict(color='#87B4E5'),xaxis=dict(color='#87B4E5'))
    return fig


# Callback for T-Bills
@app.callback(Output('Bills-Graph','figure'),
              [Input('interval-component','n_intervals')])
def update_graph_live(n):
    # Import Dataset
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    data_sc = pd.read_csv(DATA_PATH.joinpath("SOMA_hist.csv"))
    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_sc['Date'],y=data_sc['T-Bills'],fill='tozeroy',line_color='#810f7c'))
    fig["layout"][
    "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on update
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 400
    fig["layout"]["width"] = 450
    fig["layout"]["yaxis"]["gridwidth"] = 1
    fig["layout"]["yaxis"]["title"] = 'Value'
    fig["layout"]["xaxis"]["title"] = 'Date'
    fig["layout"]["yaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["xaxis"]["gridcolor"] = "#242E3F"
    fig["layout"].update(paper_bgcolor="#1D262F", plot_bgcolor="#1D262F")
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_layout(title_text='T-Bill Holdings',title_x=0.5,
    title_font_color='#87B4E5',yaxis=dict(color='#87B4E5'),xaxis=dict(color='#87B4E5'))
    return fig

# Callback for T-Notes & T-Bonds Area Graph
@app.callback(Output('T_Notes_T_Bonds','figure'),
              [Input('interval-component','n_intervals')])
def update_graph_live(n):
    # Import Dataset
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    data_sc = pd.read_csv(DATA_PATH.joinpath("SOMA_hist.csv"))
    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_sc['Date'],y=data_sc['T-Notes & T-Bonds'],fill='tozeroy',line_color='#5c8cbe'))
    fig["layout"][
    "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on updat
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 400
    fig["layout"]["width"] = 450
    fig["layout"]["yaxis"]["gridwidth"] = 1
    fig["layout"]["yaxis"]["title"] = 'Value'
    fig["layout"]["xaxis"]["title"] = 'Date'
    fig["layout"]["yaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["xaxis"]["gridcolor"] = "#242E3F"
    fig["layout"].update(paper_bgcolor="#1D262F", plot_bgcolor="#1D262F")
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_layout(title_text='T-Note & T-Bond Holdings',title_x=0.5,
    title_font_color='#87B4E5',yaxis=dict(color='#87B4E5'),xaxis=dict(color='#87B4E5'))
    return fig

# Callback for Total Area Graph
@app.callback(Output('Total-Graph','figure'),
              [Input('interval-component','n_intervals')])
def update_graph_live(n):
    # Import Dataset
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    data_sc = pd.read_csv(DATA_PATH.joinpath("SOMA_hist.csv"))
    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_sc['Date'],y=data_sc['Total'],fill='tozeroy',line_color='#810f7c'))
    fig["layout"][
    "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on update
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 400
    fig["layout"]["width"] = 500
    fig["layout"]["yaxis"]["gridwidth"] = 1
    fig["layout"]["yaxis"]["title"] = 'Value'
    fig["layout"]["xaxis"]["title"] = 'Date'
    fig["layout"]["yaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["xaxis"]["gridcolor"] = "#242E3F"
    fig["layout"].update(paper_bgcolor="#1D262F", plot_bgcolor="#1D262F")
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_layout(title_text='Total SOMA Holdings',title_x=0.5,
    title_font_color='#87B4E5',yaxis=dict(color='#87B4E5'),xaxis=dict(color='#87B4E5'))
    return fig


# Callback for soma bargraph
@app.callback(Output('soma-bargraph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_soma_change(n):
    # Import dataset
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    data_sc = pd.read_csv(DATA_PATH.joinpath("SOMA.csv"))
    data_sc = data_sc[:7]
    # Plotting
    fig = px.bar(data_sc,x='Security',y='Value',color_discrete_sequence=['#5c8cbe'])
    fig["layout"][
    "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on updat
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 400
    fig["layout"]["width"] = 500
    fig["layout"]["yaxis"]["gridwidth"] = 1
    fig["layout"]["yaxis"]["title"] = 'Value'
    fig["layout"]["xaxis"]["title"] = 'Security'
    fig["layout"]["yaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["xaxis"]["gridcolor"] = "#242E3F"
    fig["layout"].update(paper_bgcolor="#1D262F", plot_bgcolor="#1D262F")
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_layout(title_text='Federal Reserve SOMA Portfolio',title_x=0.5,
    title_font_color='#87B4E5',yaxis=dict(color='#87B4E5'),xaxis=dict(color='#87B4E5'))
    return fig


# Callback function to update command bar
@app.callback(Output("output4", "children"), [Input("input4", "value")])
def output_text(value):
    if value == "/esChain":
        return dcc.Location(id='test',pathname='/apps/esChain')
    if value == "/home":
        return dcc.Location(id='home__',pathname='/apps/home')
    if value == "/USTCurve":
        return dcc.Location(id="USTCurve",pathname='/apps/USTCurve')
    if value == "/portfolio":
        return dcc.Location(id="portfolio",pathname='/apps/porfolio')
    if value == "/soma":
    	return "Already on soma page"
    if value == None:
        print('Enter Command in searchbar')
    else:
        print('incorrect command!')

# Callback to update live clock
@app.callback(Output("live_clock4", "children"), [Input("interval", "n_intervals")])
def update_time(n):
    return datetime.datetime.now().strftime("%H:%M:%S")

# Callback to update news
@app.callback(Output("news4", "children"), [Input("i_news", "n_intervals")])
def update_news_div(n):
    return update_news()
#------------------------------------
