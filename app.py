import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.config.suppress_callback_exceptions = True