#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2018-2024 by mundialis GmbH & Co. KG

SPDX-License-Identifier: GPL-3.0-or-later

First test
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"

import pytest

from actinia_example_plugin.core.example import transform_input


@pytest.mark.unittest
@pytest.mark.parametrize(
    ("inp", "ref_out"),
    [("test", "Hello world TEST!"), ("bla23", "Hello world BLA23!")],
)
def test_transform_input(inp: str, ref_out: str) -> None:
    """Test for tranform_input function."""
    out = transform_input(inp)
    assert out == ref_out, f"Wrong result from transform_input for {inp}"
