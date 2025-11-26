#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2018-2025 by mundialis GmbH & Co. KG

SPDX-License-Identifier: GPL-3.0-or-later

actinia plugin initalization
"""

__license__ = "GPLv3"
__author__ = "Carmen Tawalika, Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


import importlib.metadata

try:
    # Change here if project is renamed and does not equal the package name
    DIST_NAME = __name__
    __version__ = importlib.metadata.version(DIST_NAME)
except Exception():
    __version__ = "unknown"
