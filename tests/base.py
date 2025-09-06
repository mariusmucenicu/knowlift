"""
Base test classes for common testing functionality.

This module provides base test classes that offer shared setup and teardown
logic for different types of tests in the application.

Classes
-------
AppTestCase
    Base test case providing Flask app setup with database engine and test client.
ModelTestCase
    Pure model test case with database engine and model creation.
"""

# Standard library
import unittest

# Project specific
from knowlift import web
from knowlift.core import settings
from knowlift.data import models


class AppTestCase(unittest.TestCase):
    """Base test case with Flask app setup and database engine."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.app = web.create_app(env='test')
        cls.engine = cls.app.config['DATABASE_ENGINE']

    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.engine.dispose()
        finally:
            super().tearDownClass()


class ModelTestCase(unittest.TestCase):
    """Base test case for model testing with database engine and model creation."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_config = settings.get_config('test')
        cls.engine = app_config.DATABASE_ENGINE
        models.metadata.create_all(cls.engine)

    def setUp(self):
        super().setUp()
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()

    def tearDown(self):
        self.transaction.rollback()
        self.connection.close()
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.engine.dispose()
        finally:
            super().tearDownClass()
