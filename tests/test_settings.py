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
"""

# Standard library
import os
import unittest
import unittest.mock

# Project specific
from knowlift.core import settings

PRODUCTION_MOCK_ENV_VARS = {
    "KNOWLIFT_DATABASE": "production.db",
    "KNOWLIFT_SECRET_KEY": "super-secret-prod-key",
}


class ConfigTestBaseMixin:
    """
    Common assertions for all config classes.
    """

    CONFIG_CLS = None

    EXPECTED_TESTING = None
    EXPECTED_DATABASE = None
    EXPECTED_DATABASE_URL = None
    EXPECTED_ROOT_LOG_LEVEL = None
    EXPECTED_ROOT_LOG_HANDLERS = None
    EXPECTED_SECRET_KEY = None

    def setUp(self):
        super().setUp()
        self.cfg = self.CONFIG_CLS()

    def test_testing_flag(self):
        """Verify TESTING flag matches expected value."""
        self.assertEqual(self.cfg.TESTING, self.EXPECTED_TESTING)

    def test_database_path(self):
        """Verify DATABASE path matches expected value."""
        self.assertEqual(self.cfg.DATABASE, self.EXPECTED_DATABASE)

    def test_database_url(self):
        """Verify DATABASE_URL matches expected value."""
        self.assertEqual(self.cfg.DATABASE_URL, self.EXPECTED_DATABASE_URL)

    def test_secret_key(self):
        """Verify SECRET_KEY matches expected value."""
        self.assertEqual(self.cfg.SECRET_KEY, self.EXPECTED_SECRET_KEY)

    def test_database_engine(self):
        """Verify DATABASE_ENGINE URL matches expected value."""
        engine_url = self.cfg.DATABASE_ENGINE.url.render_as_string()
        self.assertEqual(engine_url, self.EXPECTED_DATABASE_URL)

    def test_logging_config(self):
        """Verify logging config contains expected level and handlers."""
        root = self.cfg.LOGGING_CONFIG["root"]
        self.assertEqual(root["level"], self.EXPECTED_ROOT_LOG_LEVEL)
        self.assertEqual(root["handlers"], self.EXPECTED_ROOT_LOG_HANDLERS)

    def test_logging_config_structure(self):
        """Verify logging config has required structure."""
        config = self.cfg.LOGGING_CONFIG
        self.assertIn("version", config)
        self.assertIn("formatters", config)
        self.assertIn("handlers", config)
        self.assertIn("root", config)
        self.assertEqual(config["version"], 1)


class TestConfigDefault(ConfigTestBaseMixin, unittest.TestCase):
    """Test base Config class functionality."""

    CONFIG_CLS = settings.Config

    EXPECTED_TESTING = None
    EXPECTED_DATABASE = None
    EXPECTED_DATABASE_URL = None
    EXPECTED_ROOT_LOG_LEVEL = "DEBUG"
    EXPECTED_ROOT_LOG_HANDLERS = ["null"]
    EXPECTED_SECRET_KEY = None

    def test_database_engine(self):
        """Verify DATABASE_ENGINE is None for base config."""
        self.assertIsNone(self.cfg.DATABASE_ENGINE)


class TestConfigDevelopment(ConfigTestBaseMixin, unittest.TestCase):
    """Test development configuration class functionality."""

    CONFIG_CLS = settings.DevelopmentConfig

    BASE_DIR = settings.DevelopmentConfig.BASE_DIR
    EXPECTED_TESTING = False
    EXPECTED_DATABASE = os.path.join(BASE_DIR, "development.db")
    EXPECTED_DATABASE_URL = f"sqlite:///{EXPECTED_DATABASE}"
    EXPECTED_ROOT_LOG_LEVEL = "DEBUG"
    EXPECTED_ROOT_LOG_HANDLERS = ["default"]
    EXPECTED_SECRET_KEY = "q3J8v4oX8dK2Yf1L7eJ0w9rQ5mT2pA6sC3uV1bH4zE8I="


class TestConfigTesting(ConfigTestBaseMixin, unittest.TestCase):
    """Test testing configuration class functionality."""

    CONFIG_CLS = settings.TestConfig

    BASE_DIR = settings.TestConfig.BASE_DIR
    EXPECTED_TESTING = True
    EXPECTED_DATABASE = os.path.join(BASE_DIR, "test.db")
    EXPECTED_DATABASE_URL = f"sqlite:///{EXPECTED_DATABASE}"
    EXPECTED_ROOT_LOG_LEVEL = "DEBUG"
    EXPECTED_ROOT_LOG_HANDLERS = ["null"]
    EXPECTED_SECRET_KEY = None


class TestConfigProduction(ConfigTestBaseMixin, unittest.TestCase):
    """Test production configuration class functionality."""

    CONFIG_CLS = settings.ProductionConfig

    EXPECTED_TESTING = False
    EXPECTED_DATABASE = "production.db"
    EXPECTED_DATABASE_URL = f"sqlite:///{EXPECTED_DATABASE}"
    EXPECTED_ROOT_LOG_LEVEL = "INFO"
    EXPECTED_ROOT_LOG_HANDLERS = ["default"]
    EXPECTED_SECRET_KEY = "super-secret-prod-key"

    @unittest.mock.patch.dict("os.environ", PRODUCTION_MOCK_ENV_VARS)
    def setUp(self):
        super().setUp()

    def test_validate_with_valid_config(self):
        """Test that validation passes when all required values are present."""
        self.cfg._validate()

    def test_validate_missing_secret_key(self):
        """Test that RuntimeError is raised when SECRET_KEY is missing."""
        self.cfg.SECRET_KEY = None

        with self.assertRaises(RuntimeError) as context:
            self.cfg._validate()

        exception_message = str(context.exception)
        expected_error_message = "SECRET_KEY is required in production."
        self.assertEqual(exception_message, expected_error_message)

    def test_validate_empty_secret_key(self):
        """Test that RuntimeError is raised when SECRET_KEY is empty."""
        self.cfg.SECRET_KEY = ""

        with self.assertRaises(RuntimeError) as context:
            self.cfg._validate()

        exception_message = str(context.exception)
        expected_error_message = "SECRET_KEY is required in production."
        self.assertEqual(exception_message, expected_error_message)

    def test_validate_missing_database(self):
        """Test that RuntimeError is raised when DATABASE is missing."""
        self.cfg.DATABASE = None

        with self.assertRaises(RuntimeError) as context:
            self.cfg._validate()

        exception_message = str(context.exception)
        expected_error_message = "DATABASE is required in production."
        self.assertEqual(exception_message, expected_error_message)

    def test_validate_empty_database(self):
        """Test that validation raises RuntimeError when DATABASE is empty."""
        self.cfg.DATABASE = ""

        with self.assertRaises(RuntimeError) as context:
            self.cfg._validate()

        exception_message = str(context.exception)
        expected_error_message = "DATABASE is required in production."
        self.assertEqual(exception_message, expected_error_message)


class GetConfigFunctionTests(unittest.TestCase):
    """Test the get_config function for environment selection."""

    def tearDown(self):
        settings.get_config.cache_clear()
        super().tearDown()

    def test_get_config_by_environment(self):
        """Test config retrieval by environment name."""
        cases = [
            ("development", settings.DevelopmentConfig),
            ("test", settings.TestConfig),
        ]

        for env_name, expected_class in cases:
            with self.subTest(environment=env_name):
                cfg = settings.get_config(env_name)
                self.assertIsInstance(cfg, expected_class)

    @unittest.mock.patch.dict("os.environ", PRODUCTION_MOCK_ENV_VARS)
    def test_get_config_production(self):
        """Test production config with environment variables."""
        cfg = settings.get_config("production")
        self.assertIsInstance(cfg, settings.ProductionConfig)

    def test_get_config_case_insensitive(self):
        """Test config retrieval with case insensitive environment names."""
        cfg_upper = settings.get_config("DEVELOPMENT")
        cfg_mixed = settings.get_config("Development")
        self.assertIsInstance(cfg_upper, settings.DevelopmentConfig)
        self.assertIsInstance(cfg_mixed, settings.DevelopmentConfig)

    def test_get_config_strips_whitespace(self):
        """Test config retrieval strips whitespace from environment names."""
        cfg = settings.get_config("   development   ")
        self.assertIsInstance(cfg, settings.DevelopmentConfig)

    def test_get_config_default_fallback(self):
        """Test config fallback to development for unknown environments."""
        cfg = settings.get_config("unknown-env-name")
        self.assertIsInstance(cfg, settings.DevelopmentConfig)

    def test_get_config_is_cached(self):
        """Test config instances are cached and reused."""
        cfg1 = settings.get_config("development")
        cfg2 = settings.get_config("development")
        self.assertIs(cfg1, cfg2)

        cfg3 = settings.get_config("test")
        self.assertIsNot(cfg1, cfg3)
