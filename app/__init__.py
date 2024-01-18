import dash_bootstrap_components as dbc
import flask
from dash import Dash
from app.components.layout import create_layout


external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400&display=swap",
    dbc.themes.BOOTSTRAP,
]

server = flask.Flask(__name__)
app = Dash(external_stylesheets=external_stylesheets, server=server, update_title=None)
app.title = "RTS Dashboard"
app.layout = create_layout()
from app import callbacks
