# Example Code for Testing Strategies for Python

This example code uses Python's [unittest](https://docs.python.org/3/library/unittest.html?highlight=discover#) to demonstrate how to use the bultin framework to write and run unit tests for a simple pug class.

## Prerequisites

1. Install [pipenv](https://pipenv.pypa.io/en/latest/): `python3 pip install pipenv`

## Setup

1. Activate virtual environment: `pipenv shell`
2. Install dependencies from Pipfile.lock: `pipenv install`
3. (Deactivate virtual environment: `exit`)

## Useful commands

* To [discover](https://docs.python.org/3/library/unittest.html?highlight=discover#unittest.TestLoader.discover) and run the tests: `python3 -m unittest`
* To execute [coverage](https://coverage.readthedocs.io/en/7.3.1/index.html) on unit tests (using discovery): `python3 -m coverage run -m unittest`
* To generage a coverage report: `python3 -m coverage report`

![alt text](static/img/money-pug.gif)