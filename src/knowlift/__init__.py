# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
This application follows a hybrid architecture combining onion and layered
patterns with clear separation of concerns across packages.

Packages
--------
web: Presentation layer
    Validates input data, composes responses, formats output data.
data: Data layer
    Database initialization, ORM models, and model helpers.
domain: Business logic layer
    Core business rules and domain-specific algorithms.
core: Configuration package
    Application configuration and settings for startup and runtime.
"""
