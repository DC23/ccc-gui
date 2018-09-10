# Car Cost Calculator GUI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Dash GUI for the Car Cost Calculator

## Development Environment

1. First, clone [car-cost-calculator](https://github.com/DC23/car-cost-calculator) to a directory alongside this project.
2. Then create the Python virtual environment with [Pipenv](https://pipenv.readthedocs.io/en/latest/):

```shell
pipenv install --dev
```

3. To install [`black`](https://github.com/ambv/black) for code formatting, you need to install manually with pip after creating the main environment with pipenv. This is because `black` seems to be permanently in pre-release mode and I don't want to globally enable pre-releases in the `Pipfile`. The command is:

```shell
pipenv run pip install black
```

## Run

Check that the virtual environment is activated, then run:

```shell
cd ccc_gui
python app.py
```

## Code formatting

To format all python files, run:

```shell
black .
```

## Deploy on Heroku

Follow the [Dash deployment guide](https://dash.plot.ly/deployment) or have a look at the [dash-heroku-template](https://github.com/plotly/dash-heroku-template)
