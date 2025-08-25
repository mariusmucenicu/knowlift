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


def init_db(database_url):
    """
    Initialize the database schema and engine.

    :param database_url: Database connection string
    :type database_url: str

    :return: The newly configured database engine
    :rtype: sqlalchemy.engine.Engine

    .. note::
       - Safe to call multiple times
       - Existing tables are left unchanged, even if model definitions differ
    """

    database_engine = sqlalchemy.create_engine(database_url)
    models.metadata.create_all(bind=database_engine)

    logger.debug(
        'Engine name: %s | Engine driver: %s | Database: %s',
        database_engine.name,
        database_engine.driver,
        database_engine.url,
    )
    return database_engine
