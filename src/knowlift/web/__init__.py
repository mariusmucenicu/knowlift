# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
The web package validates input data, composes responses, formats output data.

Functions
---------
create_app
    Create and configure a Flask application.

Modules
-------
views
    Handle HTTP requests.
connections
    Database connection management.

Notes
-----
- Database connections are automatically closed via Flask's teardown handlers.
- The database engine is stored in Flask's config for application-wide access.

Miscellaneous objects
---------------------
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
from knowlift.core import settings
from knowlift.web import connections
from knowlift.web import views


def create_app(env=None):
    """
    Configure, register, and return the Flask application.

    Configuration precedence (low → high):
        1. Environment base class (Production/Development/Test)
        2. instance/local_settings.py (if present)
        3. Prefixed environment variables (KNOWLIFT_*) — highest precedence

    Args:
        env (str | None):
            Environment name ('development', 'production', or 'test').
            If None, uses KNOWLIFT_ENV or defaults to 'production'.

    Returns:
        flask.app.Flask: The Flask WSGI application instance.
    """
    app = flask.Flask(
        'knowlift',
        instance_relative_config=True,
        template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
        static_folder=os.path.join(os.path.dirname(__file__), 'static')
    )

    app_environment = env or os.getenv('KNOWLIFT_ENV', 'production')
    app_config = settings.get_config(app_environment)

    app.config.from_object(app_config())
    app.config.from_pyfile('local_settings.py', silent=True)
    app.config.from_prefixed_env(prefix='KNOWLIFT')

    logging_config.dictConfig(app.config['LOGGING_CONFIG'])

    app.add_url_rule('/', 'index', views.index)
    app.add_url_rule('/about', 'about', views.about)
    app.add_url_rule('/grade', 'grade', views.grade)
    app.add_url_rule('/ladder', 'ladder', views.ladder)
    app.add_url_rule('/legal', 'legal', views.legal)
    app.add_url_rule('/play', 'play', views.play, methods=['POST'])
    app.add_url_rule('/result', 'result', views.result, methods=['POST'])

    app.register_error_handler(404, views.page_not_found)
    app.register_error_handler(500, views.internal_server_error)

    app.teardown_appcontext(connections.close_db_connection)
    return app
