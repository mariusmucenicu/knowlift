# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
Store logic that facilitates interaction with the underlying database.

Functions:
==========
    close_connection: Close the DB API connection.
    get_connection: Get or create a single DB API connection.
    init_db: Initialize the database.


Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
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
    Get or create a single DB API connection checked out from the connection pool.

    :return: A new DB API Connection object.
    :rtype: sqlalchemy.engine.base.Connection
    """
    if 'db' not in flask.g:
        engine = flask.current_app.config['DATABASE_ENGINE']
        flask.g.db = engine.connect()
        return flask.g.db
    else:
        return flask.g.db


def close_connection(exception):
    """Return the underlying DB API connection to the connection pool."""
    if exception:
        logger.error(exception)

    db = getattr(flask.g, 'db', None)
    if db is not None:
        db.close()
    else:
        logger.debug('The database does not exist on the application context.')


def init_db(app):
    """
    Initialize the database.

    This procedure does the following:
        - Creates all the tables bound to a metadata and their associated schema constructs.
        - Creates the database engine & loads it in the flask config, where it's held globally for
            the lifetime of the application.

    Notes
    =====
        - models.metadata is a container object that keeps together many features of a database.
        - The engine object created below is a mechanism that provides db connectivity and behavior.

    This procedure is safe to be called multiple times, as, by default, will not attempt to recreate
        tables that are already present in the target database. Rebooting the server during
        development or production won't affect the database.

    :param app: A Flask application.
    :type app: flask.app.Flask
    """
    assertion_error = (
        'The database was either not set or explicitly sent as an empty string in order to create'
        ' an in-memory database.\nNote that in-memory databases should only be used in interactive'
        ' mode (via CLI) and not with this application.'
    )
    assert app.config['DATABASE'], assertion_error
    database_engine = sqlalchemy.create_engine(f"sqlite:///{app.config['DATABASE']}")
    models.metadata.create_all(bind=database_engine)
    app.config['DATABASE_ENGINE'] = database_engine
    logger.debug(
        f'Engine name: {database_engine.name}, '
        f'Engine driver: {database_engine.driver}, '
        f'Database: {database_engine.url}, '
        f'Current database tables: {database_engine.table_names()}',
    )
