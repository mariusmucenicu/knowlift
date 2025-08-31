# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
Handle incoming HTTP requests.

Functions
---------
index
    Get the homepage.
internal_server_error
    Get the custom internal server error page.
about
    Get the about page.
grade
    Get the grade page (this page contains all the difficulty levels).
ladder
    Get the ladder page.
legal
    Get the legal page (this page comprises legal information e.g GDPR, terms of use, etc).
page_not_found
    Get the custom not found page.
play
    Return a mathematical interval based on a particular difficulty level.
result
    Return a result based on the user's input.

Module Variables
----------------
logger
    An object that exposes several methods that can be used to log messages at runtime.

Notes
-----
Except for the public objects exported by this module and their public APIs (if applicable),
everything else is an implementation detail, and shouldn't be relied upon as it may change
over time.
"""

# Standard library
import logging
import json

# Third-party
import flask

# Project specific
from knowlift.application import interval_count

logger = logging.getLogger(__name__)


def index():
    return flask.render_template('index.html')


def about():
    return flask.render_template('about.html')


def grade():
    return flask.render_template('grade.html')


def ladder():
    return flask.render_template('ladder.html')


def legal():
    return flask.render_template('legal.html')


def page_not_found(e):
    e.description = f'The following URL: {flask.request.url} was not found on the server.'
    logger.error(e)
    return flask.render_template('404.html'), 404


def internal_server_error(e):
    logger.error(e)
    return flask.render_template('500.html'), 500


def play():
    """
    Build a mathematical interval from a difficulty level. The difficulty level is represented by an
        integer which in turn is mapped to a tuple that contains the interval's limits.

    :return: A template containing either the interval in the form of a question or a custom error.
    :rtype: str
    """
    level = flask.request.form.get('level')
    data = interval_count.start_game(level)
    if not data:
        flask.abort(500, description=f'Unable to use: {level} as a game level.')
    else:
        return flask.render_template('play.html', data=data)


def result():
    """
    Produce a result based on the user's input. Besides the user's answer, the input contains
        meta-data about the mathematical interval as well as the current game level. This is used
        both for validation purposes as well as for building further questions based on the same
        degree of difficulty.

    :return: A template containing either the appropriate result_data page or a custom error.
    :rtype: str
    """
    raw_data = flask.request.form.get('data')
    if not raw_data:
        data = {}
    else:
        data = json.loads(raw_data)

    result_data = interval_count.evaluate_answer(data)
    if not result_data:
        flask.abort(500, description=f'Unable to generate results from {raw_data}.')
    elif result_data['outcome']:
        return flask.render_template('result_correct.html', data=result_data)
    else:
        return flask.render_template('result_incorrect.html', data=result_data)
