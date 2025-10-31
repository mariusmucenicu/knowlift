#!/usr/bin/env python3
"""
Database initialization script.

Creates all tables defined in the application's metadata.
"""

# Standard library
import logging
import os

# Project specific
from knowlift.core import settings
from knowlift.data import models

logger = logging.getLogger(__name__)


def main():
    """Initialize database tables."""
    env = os.getenv('KNOWLIFT_ENV', 'development')

    app_config = settings.get_config(env)
    engine = app_config.DATABASE_ENGINE

    logger.info("Initializing database for %s environment...", env)
    logger.info("Database URL: sqlite:///%s", app_config.DATABASE)

    try:
        models.metadata.create_all(engine)
        logger.info("Database tables created successfully!")
    finally:
        engine.dispose()


if __name__ == '__main__':
    main()
