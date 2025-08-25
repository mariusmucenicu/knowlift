"""
Unit tests for the knowlift.data package.

These tests verify the functionality of the data access layer, including
database initialization, queries, and data manipulation.

Classes
-------
DataUtilsTests
    Test suite for data utility functions in the knowlift.data package.
"""

# Standard library
import unittest

# Third-party
import sqlalchemy

# Project specific
from knowlift import data


class DataUtilsTests(unittest.TestCase):
    """
    Tests that verify the behavior of various data utilities.

    Methods
    -------
    test_init_db_with_valid_config
        Ensures the DB engine is created with a valid URL.
    test_init_db_with_invalid_config
        Ensures an error is raised for a misconfigured URL.
    """

    def test_init_db_with_valid_config(self):
        """Database engine is initialized correctly with a valid config."""
        database_url = 'sqlite:///:memory:'
        engine = data.init_db(database_url)
        self.assertIsInstance(engine, sqlalchemy.engine.Engine)

    def test_init_db_with_invalid_config(self):
        """A misconfigured database URL raises an error."""
        invalid_url = ''
        with self.assertRaises(sqlalchemy.exc.ArgumentError):
            data.init_db(invalid_url)
