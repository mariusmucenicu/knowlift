# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Database logical structure (tables / relations / entities).

Module Variables
----------------
metadata
    Collection of Table objects with their schema constructs.
user
    User entity and its attributes / relationships.
country
    Country entity and its attributes / relationships.

Notes
-----
All tables must reach at least 3NF to reduce redundancy and improve integrity.
"""

# Standard library
import datetime

# Third party
import sqlalchemy

metadata = sqlalchemy.MetaData()


def utc_now():
    return datetime.datetime.now(datetime.UTC)


user = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column(
        "id",
        sqlalchemy.Integer,
        primary_key=True,
    ),
    sqlalchemy.Column(
        "username",
        sqlalchemy.String(length=255),
        unique=True,
        nullable=False,
    ),
    sqlalchemy.Column(
        "email",
        sqlalchemy.String,
        unique=True,
        nullable=False,
    ),
    sqlalchemy.Column(
        "password",
        sqlalchemy.String,
        nullable=False,
    ),
    sqlalchemy.Column(
        "country_id",
        sqlalchemy.ForeignKey("country.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "date_created",
        sqlalchemy.DateTime,
        default=utc_now,
    ),
    sqlalchemy.Column(
        "last_updated",
        sqlalchemy.DateTime,
        default=utc_now,
    ),
    sqlalchemy.Column(
        "last_login",
        sqlalchemy.DateTime,
    ),
    sqlalchemy.Column(
        "is_active",
        sqlalchemy.Boolean,
        default=False,
    ),
    sqlalchemy.Column(
        "is_staff",
        sqlalchemy.Boolean,
        default=False,
    ),
    sqlalchemy.Column(
        "first_name",
        sqlalchemy.String(length=150),
    ),
    sqlalchemy.Column(
        "last_name",
        sqlalchemy.String(length=150),
    ),
)

country = sqlalchemy.Table(
    "country",
    metadata,
    sqlalchemy.Column(
        "id",
        sqlalchemy.Integer,
        primary_key=True,
    ),
    sqlalchemy.Column(
        "english_short_name",
        sqlalchemy.String,
        unique=True,
        nullable=False,
    ),
    sqlalchemy.Column(
        "alpha2_code",
        sqlalchemy.String(length=2),
        unique=True,
        nullable=False,
    ),
    sqlalchemy.Column(
        "alpha3_code",
        sqlalchemy.String(length=3),
        unique=True,
        nullable=False,
    ),
    sqlalchemy.CheckConstraint(
        "length(alpha2_code) = 2",
        name="country_alpha2_max_length",
    ),
    sqlalchemy.CheckConstraint(
        "length(alpha3_code) = 3",
        name="country_alpha3_max_length",
    ),
)
