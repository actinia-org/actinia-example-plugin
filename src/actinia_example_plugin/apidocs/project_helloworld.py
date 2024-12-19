#!/usr/bin/env python
"""Copyright (c) 2018-present mundialis GmbH & Co. KG.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Hello World class
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2024 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


from actinia_example_plugin.model.response_models import (
    SimpleStatusCodeResponseModel,
)

describe_project_hello_world_get_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["example"],
    "description": "Project Hello World example",
    "parameters": [
        {
            "name": "project_name",
            "description": "The project name that contains the data that "
            "should be processed",
            "required": True,
            "in": "path",
            "type": "string",
            "default": "nc_spm_08",
        },
    ],
    "responses": {
        "200": {
            "description": "This response returns the string 'Hello World!'",
            "schema": SimpleStatusCodeResponseModel,
        },
    },
}

describe_project_hello_world_post_docs = {
    # "summary" is taken from the description of the get method
    "tags": ["example"],
    "description": "Project Hello World example with name",
    "parameters": [
        {
            "name": "project_name",
            "description": "The project name that contains the data that "
            "should be processed",
            "required": True,
            "in": "path",
            "type": "string",
            "default": "nc_spm_08",
        },
    ],
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
