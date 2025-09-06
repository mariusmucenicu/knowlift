# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Implement the logical structure of the database.

Module Variables
----------------
metadata
    A collection of Table objects and their associated schema constructs.
user
    The user entity with its corresponding attributes and relationships.
country
    The country entity with its corresponding attributes and relationships.

Notes
-----
It's imperative that the tables (relations/entities) below achieve at least 3NF in order to
reduce data redundancy and improve data integrity.

Except for the public objects exported by this module and their public APIs (if applicable),
everything else is an implementation detail, and shouldn't be relied upon as it may change
over time.
"""

# Standard library
import datetime

# Third party
import sqlalchemy


metadata = sqlalchemy.MetaData()

user = sqlalchemy.Table(
    'user',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('username', sqlalchemy.String(length=255), unique=True, nullable=False),
    sqlalchemy.Column('email', sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column('password', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('country_id', sqlalchemy.ForeignKey('country.id'), nullable=False),
    sqlalchemy.Column('date_created', sqlalchemy.DateTime, default=lambda: datetime.datetime.now(datetime.UTC)),
    sqlalchemy.Column('last_updated', sqlalchemy.DateTime, default=lambda: datetime.datetime.now(datetime.UTC)),
    sqlalchemy.Column('last_login', sqlalchemy.DateTime),
    sqlalchemy.Column('is_active', sqlalchemy.Boolean, default=False),
    sqlalchemy.Column('is_staff', sqlalchemy.Boolean, default=False),
    sqlalchemy.Column('first_name', sqlalchemy.String(length=150)),
    sqlalchemy.Column('last_name', sqlalchemy.String(length=150)),
)

country = sqlalchemy.Table(
    'country',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('english_short_name', sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column('alpha2_code', sqlalchemy.String(length=2), unique=True, nullable=False),
    sqlalchemy.Column('alpha3_code', sqlalchemy.String(length=3), unique=True, nullable=False),
    sqlalchemy.CheckConstraint("length(alpha2_code) = 2", name="country_alpha2_max_length"),
    sqlalchemy.CheckConstraint("length(alpha3_code) = 3", name="country_alpha3_max_length"),
)
