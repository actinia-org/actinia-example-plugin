#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2018-2024 by mundialis GmbH & Co. KG

SPDX-License-Identifier: GPL-3.0-or-later

Hello World class
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


from actinia_example_plugin.model.response_models import (
    SimpleStatusCodeResponseModel,
)

describe_hello_world_get_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["example"],
    "description": "Hello World example",
    "responses": {
        "200": {
            "description": "This response returns the string 'Hello World!'",
            "schema": SimpleStatusCodeResponseModel,
        },
    },
}

describe_hello_world_post_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["example"],
    "description": "Hello World example with name",
    "responses": {
        "200": {
            "description": "This response returns the string 'Hello World "
            "NAME!'",
            "schema": SimpleStatusCodeResponseModel,
        },
        "400": {
            "description": "This response returns a detail error message",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "detailed message",
                        "example": "Missing name in JSON content",
                    },
                },
            },
        },
    },
}
