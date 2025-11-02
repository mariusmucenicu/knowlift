# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Store environment-based configuration (development, production, test).

Classes
-------
Config
    Store the default configuration settings. Override per-subclass.
DevelopmentConfig
    Store the development configuration settings.
ProductionConfig
    Store the production configuration settings.
TestConfig
    Store the test configuration settings.

Functions
---------
get_config
    Return configuration instance based on environment name.

Notes
-----
- These settings are required to be available when the application starts.
- Many of these settings are sensitive and must be kept confidential.
- There is a different configuration for each environment: prod, dev, test.
- The environments above tell Flask which context the app is running in.
- To switch between environments (configurations) set the KNOWLIFT_ENV env.
- If KNOWLIFT_ENV is not set, the default config used will be development.
- Do not alter settings in the application at runtime.
"""

# Standard library
import copy
import functools
import os

# Third party
import sqlalchemy


class Config:
    """
    Store the default configuration.

    Override these values in subclasses per-environment.
    """

    # In test mode, exceptions are propagated rather than being handled.
    TESTING = None

    # Absolute path to the settings module.
    SETTINGS_PATH = os.path.abspath(__file__)

    # Directory containing the settings module.
    SETTINGS_DIR = os.path.dirname(SETTINGS_PATH)

    # Absolute path to the project root on the filesystem.
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(SETTINGS_DIR)))

    # The absolute pathname of the database file to be opened.
    DATABASE = None

    # Full db connection url.
    DATABASE_URL = None

    # The SQlAlchemy database engine.
    DATABASE_ENGINE = None

    # This key is used to provide cryptographic signing (e.g to sign Cookies).
    # SECURITY WARNING: Keep this value secret in production!
    SECRET_KEY = None

    # Initial configuration for the logging machinery.
    LOGGING_CONFIG = {
        "version": 1,
        "formatters": {
            "default": {
                "format": (
                    "[%(asctime)s] %(levelname)s in %(module)s, "
                    "line %(lineno)d: %(message)s"
                )
            },
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "null": {
                "class": "logging.NullHandler",
            },
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["null"],
        },
    }


class ProductionConfig(Config):
    """
    Store the production configuration.

    Check the BaseClass for additional information on individual settings.
    """

    def __init__(self):
        super().__init__()
        self.TESTING = False
        self.SECRET_KEY = os.environ.get("KNOWLIFT_SECRET_KEY")
        self.DATABASE = os.environ.get("KNOWLIFT_DATABASE")
        self.DATABASE_URL = f"sqlite:///{self.DATABASE}"

        self._validate()

        self.DATABASE_ENGINE = sqlalchemy.create_engine(self.DATABASE_URL)
        self.LOGGING_CONFIG = self._configure_logging(self.LOGGING_CONFIG)

    def _validate(self):
        if not self.SECRET_KEY:
            raise RuntimeError("SECRET_KEY is required in production.")
        if not self.DATABASE:
            raise RuntimeError("DATABASE is required in production.")

    def _configure_logging(self, logging_config):
        logging_config = copy.deepcopy(logging_config)
        logging_config["root"]["level"] = "INFO"
        logging_config["root"]["handlers"] = ["default"]
        return logging_config


class DevelopmentConfig(Config):
    """
    Store the development configuration.

    Check the BaseClass for additional information on individual settings.
    """

    def __init__(self):
        super().__init__()
        self.TESTING = False
        self.SECRET_KEY = "q3J8v4oX8dK2Yf1L7eJ0w9rQ5mT2pA6sC3uV1bH4zE8I="
        self.DATABASE = os.path.join(Config.BASE_DIR, "development.db")
        self.DATABASE_URL = f"sqlite:///{self.DATABASE}"
        self.DATABASE_ENGINE = sqlalchemy.create_engine(self.DATABASE_URL)
        self.LOGGING_CONFIG = self._configure_logging(self.LOGGING_CONFIG)

    def _configure_logging(self, logging_config):
        logging_config = copy.deepcopy(logging_config)
        logging_config["root"]["handlers"] = ["default"]
        return logging_config


class TestConfig(Config):
    """
    Store the test configuration.

    Check the BaseClass for additional information on individual settings.
    """

    def __init__(self):
        super().__init__()
        self.TESTING = True
        self.DATABASE = os.path.join(Config.BASE_DIR, "test.db")
        self.DATABASE_URL = f"sqlite:///{self.DATABASE}"
        self.DATABASE_ENGINE = sqlalchemy.create_engine(self.DATABASE_URL)


CONFIGS = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestConfig,
}


@functools.cache
def get_config(name):
    """
    Return a configuration instance based on environment name.

    :param name: Environment name ('development', 'production', or 'test').
    :type name: str
    :return: Configuration instance for the specified environment.
    :rtype: Config
    """
    config_class = CONFIGS.get(name.strip().lower(), DevelopmentConfig)
    return config_class()
