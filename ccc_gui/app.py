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

app = Dash(name=app_name, server=server)
app.title = app_name

external_js = []

external_css = [
    "https://stackpath.bootstrapcdn.com/bootswatch/3.3.7/flatly/bootstrap.min.css",
    # "https://stackpath.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
    "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]


def create_header():
    """page header"""
    header = html.Header(
        html.Nav(
            [
                html.Div(
                    [html.Div([app_name], className="navbar-brand navbar-left")],
                    className="container",
                )
            ],
            className="navbar navbar-default navbar-fixed-top",
        )
    )
    return header


def create_form_group(label, control):
    return html.Div([label, control], className="form-group")


def create_content():
    """page content"""
    # placeholder for the input controls
    inputs = html.Div(
        [
            create_form_group(
                html.Label("Dropdown"),
                dcc.Dropdown(
                    options=[
                        {"label": "New York City", "value": "NYC"},
                        {"label": u"Montréal", "value": "MTL"},
                        {"label": "San Francisco", "value": "SF"},
                    ],
                    value="MTL",
                ),
            ),
            create_form_group(
                html.Label("Radio Items"),
                dcc.RadioItems(
                    options=[
                        {"label": "New York City", "value": "NYC"},
                        {"label": u"Montréal", "value": "MTL"},
                        {"label": "San Francisco", "value": "SF"},
                    ],
                    value="MTL",
                ),
            ),
            create_form_group(
                html.Label("Checkboxes"),
                dcc.Checklist(
                    options=[
                        {"label": "New York City", "value": "NYC"},
                        {"label": u"Montréal", "value": "MTL"},
                        {"label": "San Francisco", "value": "SF"},
                    ],
                    values=["MTL", "SF"],
                ),
            ),
            create_form_group(
                html.Label("Text Input"),
                dcc.Input(value="MTL", type="text", className="form-group"),
            ),
            create_form_group(
                html.Label("Slider"),
                dcc.Slider(
                    min=0, max=9, marks={i: str(i) for i in range(10)}, value=5
                ),
            ),
        ],
        className="col-md-4",
    )

    # placeholder for some charts
    outputs = html.Div(
        [
            dcc.Graph(
                id="graph-0",
                figure={
                    "data": [
                        {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
                        {
                            "x": [1, 2, 3],
                            "y": [2, 4, 5],
                            "type": "bar",
                            "name": u"Montréal",
                        },
                    ],
                    "layout": {"title": "Dash Data Visualization"},
                },
            )
        ],
        className="col-md-8 text-justify",
    )

    content = html.Div(
        [html.Div([inputs, outputs], className="row")],
        id="main-content",
        className="container",
    )

    return content


def create_footer():
    """page footer"""
    footer = html.Footer(
        [
            html.Div(
                [
                    html.P(
                        [
                            html.Span(
                                "{0}, version 0.1.0".format(app_name),
                                className="text-muted",
                            )
                        ],
                        className="navbar-text pull-left footer-text",
                    ),
                    html.P(
                        [
                            html.Span(className="fa fa-copyright text-muted"),
                            html.Span(" 2018, blah blah", className="text-muted"),
                        ],
                        className="navbar-text pull-right footer-text",
                    ),
                ],
            )
        ],
        id="main-footer",
        className="navbar navbar-default navbar-fixed-bottom",
    )

    return footer


def serve_layout():
    """page layout function"""
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
