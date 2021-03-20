#------------------------------------
import dash
#------------------------------------
app = dash.Dash(__name__,  meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)
server = app.server
#------------------------------------