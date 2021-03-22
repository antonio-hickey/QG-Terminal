#------------------------------------
# Import Modules                    #
#------------------------------------
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from apps import home, esChain, usRates, portfolio, soma
#------------------------------------
# Layout                            #
#------------------------------------
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
#------------------------------------
# Callbacks                         #
#------------------------------------
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/home':
        return home.layout
    elif pathname == '/apps/esChain':
        return esChain.layout
    elif pathname == '/apps/usRates':
        return usRates.layout
    elif pathname == '/apps/portfolio':
        return portfolio.layout
    elif pathname == '/apps/soma':
    	return soma.layout
    else:
        return '404'
#------------------------------------
#------------------------------------
# Running Server                    #
#------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
#------------------------------------
