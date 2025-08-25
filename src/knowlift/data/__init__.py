"""
This package implements the data layer.

It defines ORM models, utilities, and handles all data access and manipulation.

Modules
-------
- models: Define entities and relationships for application data.

Functions
---------
- init_db: Create the db engine and all tables defined in the app's metadata.

Notes
-----
Except for the public objects exported by this module and their public APIs
(if applicable), everything else is an implementation detail and should not be
relied upon, as it may change over time.
"""

# Standard library
import logging

# Third-party
import sqlalchemy

# Project specific
from knowlift.data import models

logger = logging.getLogger(__name__)


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
