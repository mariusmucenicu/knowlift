"""
Implement model factories for creating database records with default values.

The factories here aid in supporting the DRY principle throughout tests.

Functions:
==========
    create_country(connection, **kwargs) -> sqlalchemy.Row:
        Create a country record.

    create_user(connection, **kwargs) -> sqlalchemy.Row:
        Create a user record with an associated country and incremental naming.

Global Variables:
=================
    logger (logging.Logger):
        Logger instance for debugging purposes.
    infinite_sequence (itertools.count):
        Counter for generating unique sequential identifiers.

Notes:
======
    - All factory functions require an active database connection.
    - User creation automatically handles country dependencies.
    - Duplicate countries are handled gracefully by fetching existing records.
    - Sequential numbering ensures unique usernames across test runs.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public
    APIs (if applicable), everything else is an implementation detail, and
    shouldn't be relied upon as it may change over time.
"""

# Standard library
import itertools
import logging
import os

# Third party
import sqlalchemy

from sqlalchemy import exc

# Project specific
from knowlift import models

logger = logging.getLogger(__name__)

infinite_sequence = itertools.count(start=1)


def create_user(connection, **kwargs):
    """
    Create a user record with default test data and an associated country.

    Args:
        connection (sqlalchemy.Connection):
            A database connection from the connection pool.
        **kwargs:
            Optional field overrides for user or country attributes.

    Returns:
        sqlalchemy.Row:
            The created user record.

    Raises:
        sqlalchemy.exc.SQLAlchemyError:
            If db operations fail beyond expected duplicate country handling.

    Notes:
        If a country creation fails due to duplicate constraints, it fetches the
        existing country instead.
    """
    try:
        country = create_country(connection, **kwargs)
    except exc.IntegrityError as ex:
        logger.debug(
            f'Duplicate entry for country "{ex.params[0]}"'
            f' Fetching the existing one.'
        )
        country_short_name = models.country.c.english_short_name
        where_clause = country_short_name == ex.params[0]
        select_query = sqlalchemy.select(models.country).where(where_clause)
        country = connection.execute(select_query).fetchone()

    current_user = next(infinite_sequence)
    user_values = {
        'username': f'JohnWick{current_user}',
        'first_name': 'John',
        'last_name': 'Wick',
        'email': f'jw{current_user}@knowlift.com',
        'password': os.urandom(16).hex(),
        'country_id': country.id,
    }
    user_values.update(
        pair for pair in kwargs.items() if pair[0] in user_values
    )

    # insert
    insert_query = models.user.insert().values(user_values)
    connection.execute(insert_query)

    # select
    username_column = models.user.c.username
    where_clause = username_column == user_values['username']
    select_query = sqlalchemy.select(models.user).where(where_clause)
    result = connection.execute(select_query)
    return result.fetchone()


def create_country(connection, **kwargs):
    """
    Create a country record with default test data.

    Args:
        connection (sqlalchemy.Connection):
            A database connection from the connection pool.
        **kwargs:
            Optional field overrides for country attributes.

    Returns:
        sqlalchemy.Row:
            The created country record.

    Raises:
        sqlalchemy.exc.IntegrityError:
            If duplicate records exist.
        sqlalchemy.exc.SQLAlchemyError:
            If other database operations fail.
    """
    country_values = {
        'english_short_name': 'Romania',
        'alpha2_code': 'RO',
        'alpha3_code': 'ROU'
    }
    country_values.update(
        pair for pair in kwargs.items() if pair[0] in country_values
    )

    # insert
    insert_query = models.country.insert().values(country_values)
    connection.execute(insert_query)

    # select
    country_short_name = models.country.c.english_short_name
    where_clause = country_short_name == country_values['english_short_name']
    select_query = sqlalchemy.select(models.country).where(where_clause)
    result = connection.execute(select_query)
    return result.fetchone()
