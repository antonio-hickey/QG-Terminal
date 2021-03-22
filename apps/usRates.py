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
# Auction Table                     #
#------------------------------------
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df_ta = pd.read_csv(DATA_PATH.joinpath('TA.csv')) 
styles_TA = []
styles_TA.append({
            'if': {'row_index': 'odd'},
            'backgroundColor': '#1D262F'
        })
styles_TA.append({
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
                    children=[html.Div(className="news_",id="news3", children=update_news())],
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
                    dbc.Col(dbc.Input(id="input3",type="search", 
                    placeholder="Enter Command...",debounce=True)),
                    html.P(id='output3'),
                ],
                color="dark",
                dark=True,
                ),
            ],
        ),
        # Body
        html.Div(
            className = 'USTC-Chart',
            children = [
                dcc.Interval(
                    id="interval-component2",
                    interval=65000,
                    n_intervals=0
                ),
                dcc.Graph(id="USTC_Curve")
            ]
        ),

        # Testing   
        # Building a test table for treasury auction dates/times     
        html.Div(className="T_Auction",
                 children=[
                     html.Title(className="TA_title",children=["Upcoming Treasury Auctions"]),
                     dash_table.DataTable(
                                id='table',
                                columns=[{"name": i, "id": i} for i in df_ta.columns],
                                style_table = {'minHeight': '600px', 'height': '600px', 'maxHeight': '600px',
                                               'minWidth': '900px', 'width': '900px', 'maxWidth': '900px',
                                                'margin-left': '25px', 'margin-top': '-35px'},
                                style_header ={'backgroundColor':'rgb(29, 38, 47)'},
                                style_cell={'textAlign': 'center','border': '0.05px solid #5c8cbe'},
                                data = df_ta.to_dict('records'),
                                style_data_conditional=styles_TA,
                                style_as_list_view=True,
                            )
                    ]
                )
    ]
)
#------------------------------------
# Dynamic Callbacks                 #
#------------------------------------




# Callback to update UST Yield Curve
@app.callback(Output('USTC_Curve', 'figure'),
              [Input('interval-component2', 'n_intervals')])
def update_graph_live(n):
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    # UST Curve Dataset
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = date + " USTCurve.csv"
    ustc_data = pd.read_csv(DATA_PATH.joinpath(filename))
    fig = px.area(ustc_data,x='Duration',y='Yeild',color_discrete_sequence=['#810f7c'])
    fig["layout"][
        "uirevision"
    ] = "The User is always right"  # Ensures zoom on graph is the same on update
    fig["layout"]["xaxis"]["rangeslider"]["visible"] = False
    fig["layout"]["yaxis"]["range"] = [min(ustc_data['Yeild']),max(ustc_data['Yeild'])]
    fig["layout"]["margin"] = {"t": 50, "l": 50, "b": 50, "r": 25}
    fig["layout"]["autosize"] = True
    fig["layout"]["height"] = 630
    fig["layout"]["width"] = 800
    fig["layout"]["yaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["xaxis"]["gridcolor"] = "#242E3F"
    fig["layout"]["yaxis"]["gridwidth"] = 1
    fig["layout"]["yaxis"]["title"] = 'Interest Rate'
    fig["layout"]["xaxis"]["title"] = 'Duration'
    fig["layout"].update(paper_bgcolor="#1D262F", plot_bgcolor="#1D262F")
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_yaxes(title_font=dict(color='#87B4E5'))
    fig.update_layout(title_text='U.S Treasury Yield Curve',title_x=0.5,title_font_color='#87B4E5',
            yaxis=dict(color='#87B4E5'),xaxis=dict(color='#87B4E5'))
    return fig

# Callback function to update command bar
@app.callback(Output("output3", "children"), [Input("input3", "value")])
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
    	return dcc.Location(id="soma",pathname='/apps/soma')
    if value == None:
        print('Enter Command in searchbar')
    else:
        print('incorrect command!')
    print(value)
    return value

# Callback to update live clock
@app.callback(Output("live_clock3", "children"), [Input("interval", "n_intervals")])
def update_time(n):
    return datetime.datetime.now().strftime("%H:%M:%S")

# Callback to update news
@app.callback(Output("news3", "children"), [Input("i_news", "n_intervals")])
def update_news_div(n):
    return update_news()
#------------------------------------
