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
    """Creates the page header.

    Returns:
        Dash HTML Object: The Dash HTML object representing the page header.
    """

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
    # input controls
    inputs = html.Div(
        [
            html.Div(
                [
                    create_form_group(
                        html.Label("Purchase Price"),
                        dcc.Input(type="number", min=1e3, max=2e5, step=1000, value=35000),
                    ),
                    create_form_group(
                        html.Label("Fuel Economy (L/100km)"),
                        dcc.Input(type="number", min=0, max=30, step=0.1, value=6.0),
                    ),
                    create_form_group(
                        html.Label("KM per Year"),
                        dcc.Input(type="number", min=0, max=2e5, step=5000, value=15000),
                    ),
                    create_form_group(
                        html.Label("Age at Purchase"),
                        dcc.Input(type="number", min=0, max=30, step=1, value=0),
                    ),
                    create_form_group(
                        html.Label("Depreciation Rate (first 3 years)"),
                        dcc.Input(type="number", min=0, max=100, step=5, value=19),
                    ),
                    create_form_group(
                        html.Label("Depreciation Rate (after 3 years)"),
                        dcc.Input(type="number", min=0, max=100, step=5, value=10),
                    ),
                ],
                className="col-md-4",
            ),
            # html.Div(
            #     [
            #     ],
            #     className="col-md-2",
            # ),
        ]
    )

    # outputs
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
                            html.Span(" 2018, jugglindan", className="text-muted"),
                        ],
                        className="navbar-text pull-right footer-text",
                    ),
                ]
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
