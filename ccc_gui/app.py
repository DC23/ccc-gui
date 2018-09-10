"""Main app for ccc GUI"""

# pylama: ignore=W0611
from exceptions import ImproperlyConfigured
import os
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
from flask import Flask
from dash import Dash
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv

if "DYNO" in os.environ:
    # Heroku-specific config
    debug = False
else:
    # Development-mode: set debug to true and load from .env file
    debug = True
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)

# Sign in to plotly
try:
    py.sign_in(os.environ["PLOTLY_USERNAME"], os.environ["PLOTLY_API_KEY"])
except KeyError:
    raise ImproperlyConfigured("Plotly credentials not set in .env")

# app init
app_name = "Car Cost Calculator"
server = Flask(app_name)

try:
    server.secret_key = os.environ["SECRET_KEY"]
except KeyError:
    raise ImproperlyConfigured("SECRET KEY not set in .env:")

app = Dash(name=app_name, server=server, csrf_protect=True)
app.title = app_name

external_js = []

external_css = [
    "https://stackpath.bootstrapcdn.com/bootswatch/3.3.7/flatly/bootstrap.min.css",
    # "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]


def create_header():
    """page header"""
    header = html.Nav(
        [
            html.Div(
                [html.Div([app_name], className="navbar-brand navbar-left")],
                className="container",
            )
        ],
        className="navbar navbar-default navbar-fixed-top",
    )
    return header


def create_content():
    """page content"""
    inputs = html.Div(
        html.Div(
            [
                """Laboris adipisicing enim do ipsum sint adipisicing irure elit labore. Ea nisi sint irure ullamco non."""
            ],
            className="col-md-4 well",
        )
    )

    outputs = html.Div(
        [
            """Do incididunt ipsum exercitation enim eiusmod anim. Ex qui
            tempor excepteur in ea magna nulla Lorem nulla sint labore
            proident qui. Ex anim minim quis labore non qui Lorem. Ad duis
            anim officia est culpa excepteur proident officia excepteur
            laborum non. Tempor excepteur est ipsum do dolore nulla ut ipsum.
            Sint elit non excepteur tempor amet. Duis sunt commodo id id."""
        ],
        className="col-md-8 text-justify",
    )

    content = html.Div(
        [html.Div([inputs, outputs], className="row")],
        id="content",
        className="container",
        style={"padding-top": "80px"},
    )

    return content


def create_footer():
    """page footer"""
    footer = html.Footer(
        [
            html.Div(
                [
                    html.P("Footer text - LHS", className="navbar-text pull-left"),
                    html.P("Footer text - RHS", className="navbar-text pull-right"),
                ],
                className="container",
            )
        ],
        className="navbar navbar-default navbar-fixed-bottom",
    )
    return footer


def serve_layout():
    """page layout function"""
    print("serve page")
    layout = html.Div(
        [create_header(), create_content(), create_footer()],
        className="container-fluid",
    )
    return layout


app.layout = serve_layout
for js in external_js:
    app.scripts.append_script({"external_url": js})
for css in external_css:
    app.css.append_css({"external_url": css})

# TODO: callbacks

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run_server(debug=debug, port=port, threaded=True)
