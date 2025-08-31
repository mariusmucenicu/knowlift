"""
Main package for all knowlift tests.

Modules
-------
factories
    Implement model factories.
test_models
    Test knowlift.data.models functionality.
test_interval_count_game
    Test knowlift.domain.interval_count_game functionality.
test_application
    Test knowlift.application functionality.
test_web
    Test bin.webapp functionality.

Notes
-----
Except for the public objects exported by this module and their public APIs (if applicable),
everything else is an implementation detail, and shouldn't be relied upon as it may change
over time.
"""

# Standard library
import logging
import os

# Project specific
from knowlift.core import settings

try:
    os.unlink(settings.TestConfig.DATABASE)
except FileNotFoundError as ex:
    logging.debug(f'Failed to delete the database. {ex}')
