# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
This app follows a layered architecture pattern.

Packages
--------
web: Presentation layer
    Validates input data, composes responses, formats output data.
application: Application layer
    It coordinates interactions between the web layer and the domain layer.
domain: Business logic layer
    Core business rules and domain-specific algorithms.
data: Data layer
    Database initialization, ORM models, and model helpers.
core: Configuration package
    Application configuration and settings for startup and runtime.
"""
