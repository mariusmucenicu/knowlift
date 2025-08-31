"""
Unit tests for project scripts.

These tests verify the functionality of standalone scripts used for
database operations, migrations, and other administrative tasks.

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
    test_script_with_dev_and_test_environments
        Tests script behavior with development and test configurations and verifies table creation.
    """

    def test_script_with_dev_and_test_environments(self):
        """Script works correctly with development and test configurations."""
        environments = ['test', 'development']
        
        for env in environments:
            with self.subTest(environment=env):
                with mock.patch.dict(os.environ, {'KNOWLIFT_ENV': env}):
                    init_db.main()

                # Verify tables were created by checking with the appropriate config
                app_config = settings.get_config(env)()
                engine = app_config.DATABASE_ENGINE

                inspector = sqlalchemy.inspect(engine)
                tables = inspector.get_table_names()

                self.assertIn('user', tables)
                self.assertIn('country', tables)
