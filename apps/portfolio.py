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
# Portfolio Table                   #
#------------------------------------
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df_P = pd.read_csv(DATA_PATH.joinpath('portfolio.csv')) 

styles_P = []
styles_P.append({
            'if': {'row_index': 'odd'},
            'backgroundColor': '#1D262F'
        })
styles_P.append({
            'if': {'row_index': 'even'},
            'backgroundColor': '#242E3F'
        })

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
                    children=[html.Div(id="newsp", children=update_news())],
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
                    dbc.Col(dbc.Input(id="inputp",type="search", 
                    placeholder="Enter Command...",debounce=True)),
                    html.P(id='outputp'),
                ],
                color="dark",
                dark=True,
                ),
            ],
        ),
        # Body

        # Orders Panel
        html.Div(className="testTable",
         children=[
             html.Title(className="testTitle",children=["Portfolio"]),
             dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in df_P.columns],
                        style_table = {'minHeight': '600px', 'height': '600px', 'maxHeight': '600px',
                                       'minWidth': '900px', 'width': '900px', 'maxWidth': '900px',
                                        'margin-left': '25px', 'margin-top': '-35px'},
                        style_header ={'backgroundColor':'rgb(29, 38, 47)'},
                        style_cell={'textAlign': 'center','border': '0.05px solid #5c8cbe'},
                        data = df_P.to_dict('records'),
                        style_data_conditional=styles_P,
                        editable=True
                    )
            ]
        )

        # Testing   

    ]
)
#------------------------------------
# Dynamic Callbacks                 #
#------------------------------------


# Callback function to update command bar
@app.callback(Output("outputp", "children"), [Input("inputp", "value")])
def output_text(value):
    if value == "/esChain":
        return dcc.Location(id='test',pathname='/apps/esChain')
    if value == "/home":
        return dcc.Location(id='home__',pathname='/apps/home')
    if value == "/USTCurve":
        return dcc.Location(id="USTCurve",pathname='/apps/USTCurve')
    if value == None:
        print('Enter Command in searchbar')
    else:
        print('incorrect command!')
    print(value)
    return value

# Callback to update live clock
@app.callback(Output("live_clockp", "children"), [Input("interval", "n_intervals")])
def update_time(n):
    return datetime.datetime.now().strftime("%H:%M:%S")

# Callback to update news
@app.callback(Output("newsp", "children"), [Input("i_news", "n_intervals")])
def update_news_div(n):
    return update_news()
#------------------------------------