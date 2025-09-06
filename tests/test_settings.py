"""
Test configuration settings functionality.

This module validates configuration classes, environment-based settings,
and configuration retrieval mechanisms across different environments.

Classes
-------
ConfigTestBaseMixin
    Base test class with common attribute tests.
TestConfigDefault
    Test the base configuration class functionality.
TestConfigProduction
    Test production-specific configuration settings.
TestConfigDevelopment
    Test development-specific configuration settings.
TestConfigTesting
    Test testing-specific configuration settings.
GetConfigFunctionTests
    Test the get_config function for environment selection.

Miscellaneous objects
---------------------
Except for the public objects exported by this module and their public
APIs (if applicable), everything else is an implementation detail, and
shouldn't be relied upon as it may change over time.
"""

# Standard library
import os
import unittest
from unittest import mock

# Project specific
from knowlift.core import settings


PRODUCTION_MOCK_ENV_VARS = {
    "KNOWLIFT_DATABASE": "production.db",
    "KNOWLIFT_SECRET_KEY": "super-production-secret"
}


class ConfigTestBaseMixin:
    """
    Base test class with common attribute tests for configuration classes.

    Subclasses should override class attributes to define expected values.
    """

    CONFIG_CLS = None

    EXPECTED_DEBUG = None
    EXPECTED_TESTING = None
    EXPECTED_DB_SUFFIX = None
    EXPECTED_ROOT_LOG_LEVEL = None
    EXPECTED_ROOT_LOG_HANDLERS = None
    EXPECTED_SECRET_KEY = None

    def setUp(self):
        super().setUp()
        self.cfg = self.CONFIG_CLS()

    def test_debug_flag(self):
        """Verify the DEBUG flag matches the expected value."""
        self.assertEqual(self.cfg.DEBUG, self.EXPECTED_DEBUG)

    def test_testing_flag(self):
        """Verify the TESTING flag matches the expected value."""
        self.assertEqual(self.cfg.TESTING, self.EXPECTED_TESTING)

    def test_database_path(self):
        """Verify the DATABASE path and the engine configuration."""
        self.assertTrue(self.cfg.DATABASE.endswith(self.EXPECTED_DB_SUFFIX))

    def test_databse_creation(self):
        with mock.patch('knowlift.core.settings.sqlalchemy.create_engine') as mock_engine:
            mock_engine.return_value.url = f"sqlite:///{self.cfg.DATABASE}"

            self.assertTrue(str(self.cfg.DATABASE_ENGINE.url).endswith(self.cfg.DATABASE))
            self.assertIs(self.cfg.DATABASE_ENGINE, self.cfg.DATABASE_ENGINE)
            mock_engine.assert_called_once()

    def test_logging_config(self):
        """Verify the logging configuration contains the expected values."""
        root = self.cfg.LOGGING_CONFIG["root"]
        self.assertEqual(root["level"], self.EXPECTED_ROOT_LOG_LEVEL)
        self.assertEqual(root["handlers"], self.EXPECTED_ROOT_LOG_HANDLERS)

    def test_secret_key(self):
        """Verify that the SECRET_KEY exists and has appropriate value."""
        self.assertIsNotNone(self.cfg.SECRET_KEY)

    def test_logging_config_structure(self):
        """Verify that the LOGGING_CONFIG has the required structure."""
        config = self.cfg.LOGGING_CONFIG
        self.assertIn('version', config)
        self.assertIn('formatters', config)
        self.assertIn('handlers', config)
        self.assertIn('root', config)
        self.assertEqual(config['version'], 1)


class TestConfigDefault(ConfigTestBaseMixin, unittest.TestCase):
    """Test the base configuration class functionality."""

    CONFIG_CLS = settings.Config
    EXPECTED_DEBUG = False
    EXPECTED_TESTING = False
    EXPECTED_DB_SUFFIX = "default.db"
    EXPECTED_ROOT_LOG_LEVEL = "DEBUG"
    EXPECTED_ROOT_LOG_HANDLERS = ["null"]
    EXPECTED_SECRET_KEY = True


class TestConfigDevelopment(ConfigTestBaseMixin, unittest.TestCase):
    """Test development configuration class functionality."""

    CONFIG_CLS = settings.DevelopmentConfig
    EXPECTED_DEBUG = True
    EXPECTED_TESTING = False
    EXPECTED_DB_SUFFIX = "development.db"
    EXPECTED_ROOT_LOG_LEVEL = "DEBUG"
    EXPECTED_ROOT_LOG_HANDLERS = ["default"]
    EXPECTED_SECRET_KEY = True


class TestConfigTesting(ConfigTestBaseMixin, unittest.TestCase):
    """Test testing configuration class functionality."""

    CONFIG_CLS = settings.TestConfig
    EXPECTED_DEBUG = False
    EXPECTED_TESTING = True
    EXPECTED_DB_SUFFIX = "test.db"
    EXPECTED_ROOT_LOG_LEVEL = "DEBUG"
    EXPECTED_ROOT_LOG_HANDLERS = ["null"]
    EXPECTED_SECRET_KEY = True


@mock.patch.dict(os.environ, PRODUCTION_MOCK_ENV_VARS)
class TestConfigProduction(ConfigTestBaseMixin, unittest.TestCase):
    """Test production configuration class functionality."""

    CONFIG_CLS = settings.ProductionConfig
    EXPECTED_DEBUG = False
    EXPECTED_TESTING = False
    EXPECTED_DB_SUFFIX = "production.db"
    EXPECTED_ROOT_LOG_LEVEL = "INFO"
    EXPECTED_ROOT_LOG_HANDLERS = ["default"]
    EXPECTED_SECRET_KEY = True

    def test_environment_validation_raises_error(self):
        """Verify environment variables raise RuntimeError when missing or empty."""
        test_cases = [
            ("database_missing", {}, "DATABASE"),
            ("database_empty", {"KNOWLIFT_DATABASE": ""}, "DATABASE"),
            ("secret_key_missing", {}, "SECRET_KEY"),
            ("secret_key_empty", {"KNOWLIFT_SECRET_KEY": ""}, "SECRET_KEY"),
        ]
        for case_name, env_vars, config_attr in test_cases:
            with self.subTest(case=case_name):
                with mock.patch.dict(os.environ, env_vars, clear=True):
                    with self.assertRaises(RuntimeError):
                        getattr(self.cfg, config_attr)


class GetConfigFunctionTests(unittest.TestCase):
    """Test get_config function for environment-based configuration selection."""

    def test_get_config_by_environment(self):
        """Verify get_config returns correct config class for each environment."""
        test_cases = [
            ('development', settings.DevelopmentConfig),
            ('production', settings.ProductionConfig),
            ('test', settings.TestConfig),
        ]
        
        for env_name, expected_class in test_cases:
            with self.subTest(environment=env_name):
                config = settings.get_config(env_name)
                self.assertIsInstance(config, expected_class)

    def test_get_config_case_insensitive(self):
        """Verify get_config handles case-insensitive environment names."""
        config_upper = settings.get_config('DEVELOPMENT')
        config_mixed = settings.get_config('Development')
        self.assertIsInstance(config_upper, settings.DevelopmentConfig)
        self.assertIsInstance(config_mixed, settings.DevelopmentConfig)

    def test_get_config_strips_whitespace(self):
        """Verify get_config strips whitespace from environment names."""
        config = settings.get_config('  development  ')
        self.assertIsInstance(config, settings.DevelopmentConfig)

    def test_get_config_default_fallback(self):
        """Verify get_config returns ProductionConfig for unknown environments."""
        config = settings.get_config('unknown')
        self.assertIsInstance(config, settings.ProductionConfig)
