#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2018-2024 by mundialis GmbH & Co. KG.

SPDX-License-Identifier: GPL-3.0-or-later

Hello World class
"""

__license__ = "GPL-3.0-or-later"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2018-2024 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


from typing import ClassVar

from actinia_core.models.response_models import SimpleResponseModel
from actinia_rest_lib.deprecated_locations import (
    location_deprecated_decorator,
)
from flask import jsonify, make_response, request
from flask.wrappers import Response
from flask_restful_swagger_2 import Resource, swagger

from actinia_example_plugin.apidocs import project_helloworld
from actinia_example_plugin.core.example import transform_input


class ProjectHelloWorld(Resource):
    """Returns 'Hello world with project/location!'."""

    decorators: ClassVar[list] = []

    # Add decorators for deprecated GRASS GIS locations
    decorators.append(location_deprecated_decorator)

    def __init__(self) -> None:
        """Project hello world class initialisation."""
        self.msg = "Project: Hello world!"

    @swagger.doc(project_helloworld.describe_project_hello_world_get_docs)
    def get(self, project_name: str) -> Response:
        """Get 'Hello world!' as answer string."""
        msg = f"{self.msg} {project_name}"
        return make_response(
            jsonify(
                SimpleResponseModel(
                    status="200",
                    message=msg,
                ),
            ),
            200,
        )

    @swagger.doc(project_helloworld.describe_project_hello_world_post_docs)
    def post(self, project_name: str) -> Response:
        """Hello World post method with name from postbody."""
        req_data = request.get_json(force=True)
        if isinstance(req_data, dict) is False or "name" not in req_data:
            return make_response("Missing name in JSON content", 400)
        name = req_data["name"]
        msg = f"{self.msg} {transform_input(name)} {project_name}"

        return make_response(
            jsonify(
                SimpleResponseModel(
                    status="200",
                    message=msg,
                ),
            ),
            200,
        )
