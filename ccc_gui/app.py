'''Main app for ccc GUI'''

# pylint: disable=C0103
from exceptions import ImproperlyConfigured
import os
# import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
# import plotly.graph_objs as go
from flask import Flask
from dash import Dash
# from dash.dependencies import Input, Output, State
from dotenv import load_dotenv

DOTENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(DOTENV_PATH)

# Heroku-specific config
if 'DYNO' in os.environ:
    debug = False
else:
    debug = True
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

# Sign in to plotly
try:
    py.sign_in(os.environ['PLOTLY_USERNAME'], os.environ['PLOTLY_API_KEY'])
except KeyError:
    raise ImproperlyConfigured('Plotly credentials not set in .env')

# app init
app_name = 'Car Cost Calculator GUI'
server = Flask(app_name)

try:
    server.secret_key = os.environ['SECRET_KEY']
except KeyError:
    raise ImproperlyConfigured('SECRET KEY not set in .env:')

app = Dash(name=app_name, server=server, csrf_protect=False)

external_js = []

external_css = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
]


def create_header():
    '''page header'''
    header = html.Header(
        html.H1(
            children=app_name,
            # className='well',
            id='header',
            style={},
        ))
    return header


def create_content():
    '''page content'''
    inputs = html.Div(
        className='col-lg-5',
        children=[
            '''Laboris adipisicing enim do ipsum sint adipisicing irure elit labore.
            Ea nisi sint irure ullamco non.'''
        ])

    outputs = html.Div(
        className='col-lg-7',
        children=[
            '''Do incididunt ipsum exercitation enim eiusmod anim. Ex qui
            tempor excepteur in ea magna nulla Lorem nulla sint labore
            proident qui. Ex anim minim quis labore non qui Lorem. Ad duis
            anim officia est culpa excepteur proident officia excepteur
            laborum non. Tempor excepteur est ipsum do dolore nulla ut ipsum.
            Sint elit non excepteur tempor amet. Duis sunt commodo id id.''',
        ])

    content = html.Div(
        id='content', className='row', children=[
            inputs,
            outputs,
        ])

    return content


def create_footer():
    '''page footer'''
    p0 = html.P(children=[
        html.Span('Built with '),
        html.A(
            'Plotly Dash',
            href='https://github.com/plotly/dash',
            target='_blank'),
    ])

    footer = html.Footer(
        children=html.Div([p0]),
        className='footer navbar-fixed-bottom',
        style={})
    return footer


def serve_layout():
    '''page layout function'''
    print('serve page')
    layout = html.Div(
        children=[create_header(),
                  create_content(),
                  create_footer()],
        className='container',
        style={},
    )
    return layout


app.layout = serve_layout
for js in external_js:
    app.scripts.append_script({'external_url': js})
for css in external_css:
    app.css.append_css({'external_url': css})

# TODO: callbacks

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run_server(debug=debug, port=port, threaded=True)
