# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
Kick off the web application.

Notes:
======
    This file contains the code mod_wsgi is executing on startup to get the application object.

Global variables:
=================
    application: The Flask application. Acts as a central registry for views, URLs, templates, etc.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

__author__ = 'Marius Mucenicu <marius_mucenicu@yahoo.com>'

# Project specific
import knowlift

application = knowlift.create_app()
