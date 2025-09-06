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
* These settings are required to be available when the application starts.
* Many of these settings are sensitive and must be kept confidential.
* There is a different configuration for each environment: prod, dev, test.
* The environments above tell Flask which context the app is running in.
* To switch between environments (configurations) set the KNOWLIFT_ENV env.
* If KNOWLIFT_ENV is not set, the default config used will be production.
* Do not alter settings in the application at runtime.
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

    # Whether testing mode is enabled. Exceptions are propagated rather
    # than handled by Flask.
    TESTING = False

    SETTINGS_PATH = os.path.abspath(__file__)
    SETTINGS_DIR = os.path.dirname(SETTINGS_PATH)

    # Absolute path to the project root on the filesystem. Build paths
    # inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(SETTINGS_DIR)))

    # The absolute pathname of the database file to be opened.
    DATABASE = os.path.join(BASE_DIR, 'default.db')

    # The secret key is used to provide cryptographic signing (e.g used
    # to sign Cookies). SECURITY WARNING: Set this to some random bytes.
    # Keep this value secret in production!
    SECRET_KEY = (
        '261c501ff27fc199718be6a7c8d2115d349c4ef7b26ab11222d95019112a7868'
    )

    # Initial configuration for the logging machinery.
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {
            'default': {
                'format': (
                    "[%(asctime)s] %(levelname)s in %(module)s, "
                    "line %(lineno)d: %(message)s"
                )
            },
        },
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
            'null': {
                'class': 'logging.NullHandler',
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['null'],
        },
    }

    @functools.cached_property
    def DATABASE_ENGINE(self):
        """Create and return an SQLAlchemy engine."""
        database_url = f"sqlite:///{self.DATABASE}"
        return sqlalchemy.create_engine(database_url)


class ProductionConfig(Config):
    """
    Store the production configuration.

    Check the BaseClass for additional information on individual settings.
    """

    TESTING = False

    @functools.cached_property
    def DATABASE(self):
        db = os.environ.get("KNOWLIFT_DATABASE")
        if not db:
            raise RuntimeError("KNOWLIFT_DATABASE is required in production.")
        return db

    @functools.cached_property
    def SECRET_KEY(self):
        key = os.environ.get("KNOWLIFT_SECRET_KEY")
        if not key:
            raise RuntimeError("KNOWLIFT_SECRET_KEY is required in production.")
        return key

    @functools.cached_property
    def LOGGING_CONFIG(self):
        base_config = copy.deepcopy(super().LOGGING_CONFIG)
        base_config['root']['level'] = 'INFO'
        base_config['root']['handlers'] = ['default']
        return base_config


class DevelopmentConfig(Config):
    """
    Store the development configuration.

    Check the BaseClass for additional information on individual settings.
    """

    TESTING = False
    DATABASE = os.path.join(Config.BASE_DIR, 'development.db')

    @functools.cached_property
    def LOGGING_CONFIG(self):
        base_config = copy.deepcopy(super().LOGGING_CONFIG)
        base_config['root']['handlers'] = ['default']
        return base_config


class TestConfig(Config):
    """
    Store the test configuration.

    Check the BaseClass for additional information on individual settings.
    """

    TESTING = True
    DATABASE = os.path.join(Config.BASE_DIR, 'test.db')


CONFIGS = {
    'production': ProductionConfig(),
    'development': DevelopmentConfig(),
    'test': TestConfig(),
}


def get_config(name):
    """
    Return a configuration instance based on environment name.
    
    :param name: Environment name ('development', 'production', or 'test').
    :type name: str
    :return: Configuration instance for the specified environment.
    :rtype: Config
    """
    return CONFIGS.get(name.strip().lower(), CONFIGS['production'])
