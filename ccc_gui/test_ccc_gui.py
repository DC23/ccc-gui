import dash_html_components as html
from app import app


def test_layout_is_a_function_that_returns_a_div_element():
    assert isinstance(app.layout(), html.Div)
