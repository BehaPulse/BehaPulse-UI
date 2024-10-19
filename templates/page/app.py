import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# layout
# from .layout import set_layout, set_content
from .layout import set_layout

# controller
from .controller import set_controller

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
icon_css = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css"
admin_app = dash.Dash(__name__, url_base_pathname='/beha-pulse/',
                      external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css, icon_css],
                      suppress_callback_exceptions=True)

admin_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Location(id='redirect', refresh=True),
    html.Div(id='page'),
], className="w-100 vh-100")

admin_app.title = "Beha Pulse"
admin_app._favicon = "img/favicon.svg"

# layout setting
set_layout(admin_app)

# controller setting
set_controller(admin_app)
