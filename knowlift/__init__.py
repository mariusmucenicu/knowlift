# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
Bundle core modules whose logic and configuration power this application.

Functions:
==========
    create_app: Create and configure a Flask application.

Modules:
========
    db: Store logic that enables database interaction.
    models: Define entities and relationships among them.
    number_distance: Build mathematical intervals from upper and lower bounds.
    views: Handle HTTP requests.

Notes:
======
    This package bundles the core functionality of this application.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their
    public APIs (if applicable), everything else is an implementation
    detail and shouldn't be relied upon, as it may change over time.
"""

# Standard Library
import os
from logging import config as logging_config

# Third-party
import flask

# Project specific
import default_settings
from knowlift import db
from knowlift import views


def create_app(env=None):
    """
    Configure, register, and return the Flask application.

    Configuration precedence (low → high):
        1. Environment base class (Production/Development/Test)
        2. instance/settings.py (if present)
        3. Prefixed environment variables (KNOWLIFT_*) — highest precedence

    Args:
        env (str | None):
            Environment name ('development', 'production', or 'test').
            If None, uses KNOWLIFT_ENV or defaults to 'production'.

    Returns:
        flask.app.Flask: The Flask WSGI application instance.
    """
    app = flask.Flask(__name__, instance_relative_config=True)

    app_environment = env or os.getenv('KNOWLIFT_ENV', 'production')
    app.config.from_object(default_settings.get_config(app_environment))
    app.config.from_pyfile('settings.py', silent=True)
    app.config.from_prefixed_env()

    logging_config.dictConfig(app.config['LOGGING_CONFIG'])

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
