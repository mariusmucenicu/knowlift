# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
Database connection management for the web layer.

Functions
---------
get_db_connection
    Get or create a single DB API connection from the pool.
close_db_connection
    Return the DB API connection to the pool (Flask teardown).

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

# Third-party
import flask


def get_db_connection():
    """
    Get or create a single DB API connection from the connection pool.

    This function manages database connections using Flask's application
    context (flask.g). If a connection doesn't exist in the current context,
    it creates a new one using the database engine stored in the Flask
    application configuration and starts a transaction.

    Returns:
        sqlalchemy.Connection:
            A db connection object that can be used to execute SQL queries.

    Raises:
        KeyError:
            If 'DATABASE_ENGINE' is not found in the Flask app config.
        RuntimeError:
            If called outside of a Flask application context.

    Note:
        The connection and transaction are automatically stored in flask.g and
        will be reused for subsequent calls within the same request context.
    """
    if 'db' not in flask.g:
        engine = flask.current_app.config['DATABASE_ENGINE']
        flask.g.db = engine.connect()
        flask.g.db_transaction = flask.g.db.begin()
        return flask.g.db
    else:
        return flask.g.db


def close_db_connection(exception):
    """
    Return the underlying DB API connection to the connection pool.

    This function is typically used as a Flask teardown handler to ensure
    database connections and transactions are properly closed at the end of each
    request, preventing connection leaks.

    Args:
        exception (Exception | None):
            An exception that occurred during request processing, if any.
            This parameter is required by Flask's teardown handler interface
            but the function handles both success and error cases.
    """
    logger = flask.current_app.logger

    transaction = flask.g.pop('db_transaction', None)
    db = flask.g.pop('db', None)

    if transaction is not None:
        if exception is None:
            transaction.commit()
            logger.debug("Database transaction committed")
        else:
            transaction.rollback()
            logger.error("Database transaction rolled back due to: %s", exception)

    if db is not None:
        db.close()
    else:
        logger.debug('The database does not exist on the application context.')
