#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2018-2024 by mundialis GmbH & Co. KG.

SPDX-License-Identifier: GPL-3.0-or-later

Response models
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


from typing import ClassVar

from flask_restful_swagger_2 import Schema


class SimpleStatusCodeResponseModel(Schema):
    """Simple response schema to inform about status."""

    type: str = "object"
    properties: ClassVar[dict] = {
        "status": {
            "type": "number",
            "description": "The status code of the request.",
        },
        "message": {
            "type": "string",
            "description": "A short message to describes the status",
        },
    }
    required: ClassVar[list[str]] = ["status", "message"]


simple_response_example = SimpleStatusCodeResponseModel(
    status=200,
    message="success",
)
SimpleStatusCodeResponseModel.example = simple_response_example
