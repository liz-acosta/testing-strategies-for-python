# Example Code for Testing Strategies for Python

This example code uses Python's [unittest](https://docs.python.org/3/library/unittest.html?highlight=discover#) to demonstrate how to use the bultin framework to write and run unit tests for a simple pug class. The app runs with [Flask](https://flask.palletsprojects.com/en/2.3.x/quickstart/) with [Bootstrap-Flask](https://bootstrap-flask.readthedocs.io/en/stable/) (using the [Bootswatch Minty theme](https://bootswatch.com/minty/)) and incorporates the [OpenAI API](https://platform.openai.com/).

## Prerequisites

1. Install [pipenv](https://pipenv.pypa.io/en/latest/): `python3 pip install pipenv`
2. [OpenAI API key and organization](https://openai.com/blog/openai-api)

## Setup

1. Activate virtual environment: `pipenv shell`
2. Install dependencies from Pipfile.lock: `pipenv install`
3. (Deactivate virtual environment: `exit`)
4. [Add environment variables](https://pypi.org/project/python-dotenv/#getting-started) by renaming `.env_template` to `.env`
5. And replacing placeholder secrets with real secrets

## Run tests

* To [discover](https://docs.python.org/3/library/unittest.html?highlight=discover#unittest.TestLoader.discover) and run the tests: `python3 -m unittest`
* To execute [coverage](https://coverage.readthedocs.io/en/7.3.1/index.html) on unit tests (using discovery): `python3 -m coverage run -m unittest`
* To generage a coverage report: `python3 -m coverage report`

## Run locally

1. ([Activate virtual environment](https://github.com/liz-acosta/testing-strategies-for-python/tree/main#setup))
2. [Spin up the server](https://flask.palletsprojects.com/en/2.3.x/quickstart/) from root directory: `flask run`
3. Navigate to `http://localhost:5000/` in your browser

It should look like this:

![alt text](static/img/build-a-pug_screenshot.png)

## Enjoy!
![alt text](static/img/money-pug.gif)