# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
Bundle core modules that, via their logic and/or configuration make this application possible.

Functions:
==========
    create_app: Create and configure a flask application.

Modules:
========
    db: Store logic that enables database interaction.
    lexicon: Implement a mechanism for building sentences from a given lexicon.
    models: Define entities (tables/relations) and relationships among them.
    number_distance: Build mathematical intervals based on upper and lower bounds.
    views: Handle HTTP requests.

Notes:
======
    This package is intended to bundle all of the core functionality of this application.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard Library
from logging import config

# Third-party
import flask

# Project specific
from knowlift import db
from knowlift import views


def create_app():
    """
    Configure, register and return a Flask application.

    :return: A flask object which implements a WSGI application and acts as the central object.
    :rtype: flask.app.Flask
    """
    app = flask.Flask(__name__, instance_relative_config=True)

    flask_environment = f'{app.env.capitalize()}Config'
    app.config.from_object(f'default_settings.{flask_environment}')
    app.config.from_pyfile('settings.py', silent=True)

    config.dictConfig(app.config['LOGGING_CONFIG'])

    db.init_db(app)

    app.add_url_rule('/', 'index', views.index)
    app.add_url_rule('/about', 'about', views.about)
    app.add_url_rule('/grade', 'grade', views.grade)
    app.add_url_rule('/ladder', 'ladder', views.ladder)
    app.add_url_rule('/legal', 'legal', views.legal)
    app.add_url_rule('/play', 'play', views.play, methods=['POST'])
    app.add_url_rule('/result', 'result', views.result, methods=['POST'])

    app.register_error_handler(404, views.page_not_found)
    app.register_error_handler(500, views.internal_server_error)

    app.teardown_appcontext(db.close_connection)
    return app
