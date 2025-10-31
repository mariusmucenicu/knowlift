"""
Unit tests for project scripts.

Classes
-------
InitDbScriptTests
    Test suite for the database initialization script.
"""

# Standard library
import os
import unittest
from unittest import mock

# Third-party
import sqlalchemy

# Project specific
from knowlift.core import settings
from scripts import init_db


class InitDbScriptTests(unittest.TestCase):
    """
    Tests that verify the behavior of the database initialization script.

    Methods
    -------
    test_script_with_test_environment
        Tests script behavior with test config and verifies table creation.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config = settings.get_config("test")
        cls.engine = cls.config.DATABASE_ENGINE

    @mock.patch.dict(os.environ, {"KNOWLIFT_ENV": "test"})
    def test_script_with_test_environment(self):
        """Script works correctly with test configuration."""
        init_db.main()

        # Verify tables were created by checking with the test config
        inspector = sqlalchemy.inspect(self.engine)
        tables = inspector.get_table_names()
        self.assertTrue(tables)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.engine.dispose()
        finally:
            super().tearDownClass()
