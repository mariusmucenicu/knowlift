# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
Store logic that facilitates interaction with the underlying database.

Functions:
==========
    get_connection() -> sqlalchemy.Connection:
        Get or create a single DB API connection from the connection pool.

    close_connection(exception: Exception | None) -> None:
        Return the underlying DB API connection to the connection pool.

    init_db(app: flask.Flask) -> None:
        Initialize the database schema and engine configuration.

Notes:
======
    - Db connections are automatically closed via Flask's teardown handlers.
    - The db engine is stored in Flask's config for application-wide access.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public
    APIs (if applicable), everything else is an implementation detail, and
    shouldn't be relied upon as it may change over time.
"""

# Standard library
import logging

# Third-party
import flask
import sqlalchemy

# Project specific
from knowlift import models

logger = logging.getLogger(__name__)


def get_connection():
    """
    Get or create a single DB API connection from the connection pool.

    This function manages database connections using Flask's application
    context (flask.g). If a connection doesn't exist in the current context,
    it creates a new one using the database engine stored in the Flask
    application configuration.

    Returns:
        sqlalchemy.Connection:
            A db connection object that can be used to to execute SQL queries.

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
    if exception:
        logger.error(exception)

    db = getattr(flask.g, 'db', None)
    if db is not None:
        db.close()
    else:
        logger.debug('The database does not exist on the application context.')


def init_db(app):
    """
    Initialize the database schema and engine for the Flask application.

    This function performs the following operations:
        - Validates that a database path is configured
        - Creates a SQLAlchemy engine for SQLite database connectivity
        - Creates all tables defined in the application's metadata
        - Stores the engine in Flask's application configuration

    Args:
        app (flask.Flask):
            The Flask application instance to configure. Must have a
            'DATABASE' key in its config containing the path to the SQLite
            database file.

    Raises:
        AssertionError:
            If the DATABASE configuration is missing or empty.
        sqlalchemy.exc.SQLAlchemyError:
            If the db engine/table creation fails.

    Notes:
        - This function is idempotent so its safe to be call multiple times
        - Existing tables will not be recreated or modified
        - The database file will be created if it doesn't exist
    """
    assertion_error = (
        'The database path was not configured. Please set the DATABASE '
        'configuration to a valid file path.'
    )
    assert app.config['DATABASE'], assertion_error

    database_url = f"sqlite:///{app.config['DATABASE']}"
    database_engine = sqlalchemy.create_engine(database_url)
    models.metadata.create_all(bind=database_engine)

    app.config['DATABASE_ENGINE'] = database_engine

    logger.debug(
        f'Engine name: {database_engine.name} | '
        f'Engine driver: {database_engine.driver} | '
        f'Database: {database_engine.url}'
    )
