# Car Cost Calculator GUI
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://travis-ci.org/DC23/ccc-gui.svg?branch=master)](https://travis-ci.org/DC23/ccc-gui) [![Updates](https://pyup.io/repos/github/DC23/ccc-gui/shield.svg)](https://pyup.io/repos/github/DC23/ccc-gui/) [![Python 3](https://pyup.io/repos/github/DC23/ccc-gui/python-3-shield.svg)](https://pyup.io/repos/github/DC23/ccc-gui/) [![Coverage](https://codecov.io/github/DC23/ccc-gui/coverage.svg?branch=master)](https://codecov.io/github/DC23/ccc-gui?branch=master) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


Dash GUI for the Car Cost Calculator


## Development Environment
1. First, clone [car-cost-calculator](https://github.com/DC23/car-cost-calculator) to a directory alongside this project.
2. Then create the Python virtual environment with Pipenv::
    pipenv install --dev

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
