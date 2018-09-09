'''Main app for ccc GUI'''

# pylint: disable=C0103
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

DOTENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(DOTENV_PATH)

# Heroku-specific config
if "DYNO" in os.environ:
    debug = False
else:
    debug = True
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)

# Sign in to plotly
try:
    py.sign_in(os.environ["PLOTLY_USERNAME"], os.environ["PLOTLY_API_KEY"])
except KeyError:
    raise ImproperlyConfigured("Plotly credentials not set in .env")

# app init
app_name = "Car Cost Calculator GUI"
server = Flask(app_name)

try:
    server.secret_key = os.environ["SECRET_KEY"]
except KeyError:
    raise ImproperlyConfigured("SECRET KEY not set in .env:")

app = Dash(name=app_name, server=server, csrf_protect=False)

external_js = []

external_css = [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]

theme = {"font-family": "Sans", "background-color": "#e0e0e0"}


def create_header():
    '''page header'''
    header_style = {
        "background-color": theme["background-color"],
        "padding": "1.5rem"
    }
    header = html.Header(html.H1(children=app_name, style=header_style))
    return header


def create_content():
    '''page content'''
    content = html.Div(
        children=[
            # range slider with start date and end date
            html.Div(
                children=[
                    dcc.RangeSlider(
                        id="year-slider",
                        min=1990,
                        max=2018,
                        value=[2010, 2015],
                        marks={(i): f"{i}" for i in range(1990, 2018, 2)},
                    )
                ],
                style={"margin-bottom": 20},
            ),
            html.Hr(),
            html.Div(
                children=[
                    dcc.Graph(
                        id="graph-0",
                        figure={
                            "data": [
                                {
                                    "x": [1, 2, 3],
                                    "y": [4, 1, 2],
                                    "type": "bar",
                                    "name": "SF",
                                },
                                {
                                    "x": [1, 2, 3],
                                    "y": [2, 4, 5],
                                    "type": "bar",
                                    "name": u"Montréal",
                                },
                            ],
                            "layout": {
                                "title": "Dash Data Visualization"
                            },
                        },
                    )
                ],
                className="row",
                style={"margin-bottom": 20},
            ),
            html.Div(
                children=[
                    html.Div(dcc.Graph(id="graph-1"), className="six columns"),
                    html.Div(
                        dcc.Markdown("""
                        This is a markdown description created with a Dash Core Component.

                        > A {number} days of training to develop.
                        > Ten {number} days of training to polish.
                        >
                        > — Miyamoto Musashi

                        ***
                        """.format(number="thousand").replace("  ", "")),
                        className="six columns",
                    ),
                ],
                className="row",
                style={"margin-bottom": 20},
            ),
            html.Hr(),
        ],
        id="content",
        style={
            "width": "100%",
            "height": "100%"
        },
    )
    return content


def create_footer():
    footer_style = {
        "background-color": theme["background-color"],
        "padding": "0.5rem"
    }
    p0 = html.P(children=[
        html.Span("Built with "),
        html.A(
            "Plotly Dash",
            href="https://github.com/plotly/dash",
            target="_blank"),
    ])
    # p1 = html.P(
    #     children=[
    #         html.Span("Data from "),
    #         html.A("some website", href="https://some-website.com/", target="_blank"),
    #     ]
    # )

    div = html.Div([p0])
    footer = html.Footer(children=div, style=footer_style)
    return footer


def serve_layout():
    layout = html.Div(
        children=[create_header(),
                  create_content(),
                  create_footer()],
        className="container",
        style={"font-family": theme["font-family"]},
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
