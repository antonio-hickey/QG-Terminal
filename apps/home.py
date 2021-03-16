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
#------------------------------------
# News Api                          #
#------------------------------------
# API Requests for news div
news_requests = requests.get("https://newsapi.org/v2/top-headlines?sources=bloomberg&apiKey=ef2168f74e6c4824a1ff4db29eb25b07")
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
# Commands List                     #
#------------------------------------
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df_c = pd.read_csv(DATA_PATH.joinpath('commands_list.csv'))
styles_ccl = []
styles_ccl.append({
            'if': {'row_index': 'odd'},
            'backgroundColor': '#1D262F'
        })
styles_ccl.append({
            'if': {'row_index': 'even'},
            'backgroundColor': '#242E3F'
        }) 
styles_ccl.append({
            'color': 'white'
        })
#------------------------------------
# Layout                            #
#------------------------------------
# Dash App Layout
layout = html.Div(
    className="row",
    children=[
        # Interval component for live clock
        dcc.Interval(id="interval", interval=1 * 1000, n_intervals=0),
        # Interval component for graph updates
        dcc.Interval(id="i_tris", interval=1 * 5000, n_intervals=0),
        # Interval component for news updates
        dcc.Interval(id="i_news", interval=1 * 60000, n_intervals=0),
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
                    children=[html.Div(id="news", children=update_news())],
                ),
            ],
        ),
        # Right Panel Div
        # Navbar (Command Line Bar)
        html.Div(
            className="nine columns div-right-panel",
            children=[
                # Nav Bar
                # Nav Bar
                dbc.Navbar(className="cmdTest",children=
                [
                    dbc.Col(dbc.NavbarBrand("QG Terminal", href="/apps/home"), sm=3, md=2),
                    dbc.Col(dbc.Input(id="input",type="search", 
                    placeholder="Enter Command...",debounce=True)),
                    html.P(id='output'),
                ],
                color="#1D262F",
                dark=True,
                ),
            ],
        ),
        # Testing
        # Common Command's List
        html.Div(
            className="CCL", 
            children=
            [
                html.P(className='CCL-Title',children=["Common Command List"]),
                dash_table.DataTable(
                    id='Command-Table',
                    columns=[{"name": i,"id": i}for i in df_c.columns],
                    data=df_c.to_dict('records'),
                    style_data_conditional=styles_ccl,
                    style_cell = {'textAlign': 'center','border': '0.05px solid #5c8cbe'},
                    style_header={'backgroundColor':'#1D262F'}
                )
            ]
        )
    ],
)
#------------------------------------
# Dynamic Callbacks                 #
#------------------------------------
# Callback function to update command bar
@app.callback(Output("output", "children"), [Input("input", "value")])
def output_text(value):
    if value == "/esChain":
        return dcc.Location(id='test',pathname='/apps/esChain')
    if value == "/home":
        return dcc.Location(id='home__',pathname='/apps/home')
    if value == "/usRates":
        return dcc.Location(id="usRates",pathname='/apps/usRates')
    if value == "/portfolio":
        return dcc.Location(id="portfolio",pathname='/apps/portfolio')
    if value == None:
        null = []
    else:
        print('incorrect command!')

# Callback to update live clock
@app.callback(Output("live_clock", "children"), [Input("interval", "n_intervals")])
def update_time(n):
    return datetime.datetime.now().strftime("%H:%M:%S")


# Callback to update news
@app.callback(Output("news", "children"), [Input("i_news", "n_intervals")])
def update_news_div(n):
    return update_news()