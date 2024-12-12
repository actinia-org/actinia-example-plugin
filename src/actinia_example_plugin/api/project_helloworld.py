#!/usr/bin/env python
"""
Copyright (c) 2018-present mundialis GmbH & Co. KG.

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


from flask import make_response, request
from flask_restful_swagger_2 import Resource, swagger

from actinia_example_plugin.apidocs import project_helloworld
from actinia_example_plugin.model.response_models import (
    SimpleStatusCodeResponseModel,
)
from actinia_example_plugin.core.example import transform_input


class ProjectHelloWorld(Resource):
    """Returns 'Hello world with project/location!'."""

    def __init__(self) -> None:
        """Project hello world class initialisation."""
        self.msg = "Project: Hello world!"

    @swagger.doc(project_helloworld.describeProjectHelloWorld_get_docs)
    def get(self, project_name) -> SimpleStatusCodeResponseModel:
        """Get 'Hello world!' as answer string."""
        msg = f"{self.msg} {project_name}"
        return SimpleStatusCodeResponseModel(status=200, message=msg)

    @swagger.doc(project_helloworld.describeProjectHelloWorld_post_docs)
    def post(self, project_name) -> SimpleStatusCodeResponseModel:
        """Hello World post method with name from postbody."""
        req_data = request.get_json(force=True)
        if isinstance(req_data, dict) is False or "name" not in req_data:
            return make_response("Missing name in JSON content", 400)
        name = req_data["name"]
        msg = f"{self.msg} {transform_input(name)} {project_name}"

        return SimpleStatusCodeResponseModel(status=200, message=msg)
