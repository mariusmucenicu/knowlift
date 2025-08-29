# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
The web package validates input data, composes responses, formats output data.

Functions
---------
create_app
    Create and configure a Flask application.
get_connection
    Get or create a single DB API connection from the pool.
close_connection
    Return the DB API connection to the pool (Flask teardown).

Modules
-------
views
    Handle HTTP requests.

Notes
-----
- Db connections are automatically closed via Flask's teardown handlers.
- The db engine is stored in Flask's config for application-wide access.

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
from knowlift import data
from knowlift.web import views
from knowlift.core import settings


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
    app.config.from_object(settings.get_config(app_environment))
    app.config.from_pyfile('local_settings.py', silent=True)
    app.config.from_prefixed_env(prefix='KNOWLIFT')

    database_url = f"sqlite:///{app.config['DATABASE']}"
    app.config['DATABASE_ENGINE'] = data.init_db(database_url)

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

    app.teardown_appcontext(close_connection)
    return app


def get_connection():
    """
    Get or create a single DB API connection from the connection pool.

    This function manages database connections using Flask's application
    context (flask.g). If a connection doesn't exist in the current context,
    it creates a new one using the database engine stored in the Flask
    application configuration.

    Returns:
        sqlalchemy.Connection:
            A db connection object that can be used to execute SQL queries.

    Raises:
        KeyError:
            If 'DATABASE_ENGINE' is not found in the Flask app config.
        RuntimeError:
            If called outside of a Flask application context.

    Note:
        The connection is automatically stored in flask.g and will be reused
        for subsequent calls within the same request context.
    """
    if 'db' not in flask.g:
        engine = flask.current_app.config['DATABASE_ENGINE']
        flask.g.db = engine.connect()
        return flask.g.db
    else:
        return flask.g.db


def close_connection(exception):
    """
    Return the underlying DB API connection to the connection pool.

    This function is typically used as a Flask teardown handler to ensure
    database connections are properly closed at the end of each request,
    preventing connection leaks.

    Args:
        exception (Exception | None):
            An exception that occurred during request processing, if any.
            This parameter is required by Flask's teardown handler interface
            but the function handles both success and error cases.
    """
    logger = flask.current_app.logger

    if exception:
        logger.error(exception)

    db = flask.g.pop('db', None)
    if db is not None:
        db.close()
    else:
        logger.debug('The database does not exist on the application context.')