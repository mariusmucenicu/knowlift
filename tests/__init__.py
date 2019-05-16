"""
Main package for all knowlift tests.

CONSTANTS:
==========
    TEST_APPLICATION: A Python class which implements a WSGI application and acts as a central obj.

Modules:
========
    factories: Implement model factories.
    test_lexicon: Test knowlift.lexicon functionality.
    test_models: Test knowlift.models functionality.
    test_number_distance: Test knowlift.number_distance functionality.
    test_web: Test bin.webapp functionality.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard library
import logging
import os

# Project specific
import knowlift

from knowlift import default_settings

try:
    os.unlink(default_settings.DATABASE)
except FileNotFoundError as ex:
    logging.error(f'Failed to delete the database. {ex}')
finally:
    TEST_APPLICATION = knowlift.create_app(default_settings.__file__)
    # Disabling logging within the knowlift package and do the logging on the testing side.
    logging.getLogger('knowlift').setLevel(100)
