#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2018-2024 by mundialis GmbH & Co. KG.

SPDX-License-Identifier: GPL-3.0-or-later

Example core functionality
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


def transform_input(inp: str) -> str:
    """Return a transformed string as example core function.

    Args:
        inp (str): Input string to transform

    Returns:
        (str) transformed string

    """
    return f"Hello world {inp.upper()}!"
