# SPDX-FileCopyrightText: 2024 (C) Marius Mucenicu
# SPDX-License-Identifier: AGPL-3.0-or-later


"""
WSGI entry point for the Knowlift web application.

Notes:
======
    This file is executed by mod_wsgi on startup to get the application object
    for serving the Knowlift web app.

Global variables:
=================
	application:
        The Flask application instance. Acts as a central registry for views,
        URLs, templates, and other resources.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs
    (if applicable), everything else is an implementation detail, and shouldn't
    be relied upon as it may change over time.
"""

__author__ = 'Marius Mucenicu <marius_mucenicu@yahoo.com>'

# Project specific
from knowlift import web

application = web.create_app()
