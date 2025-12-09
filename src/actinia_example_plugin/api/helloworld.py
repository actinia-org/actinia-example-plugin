#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2018-2025 by mundialis GmbH & Co. KG.

SPDX-License-Identifier: GPL-3.0-or-later

Hello World class
"""

__license__ = "GPL-3.0-or-later"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2018-2025 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


from flask import make_response, request
from flask_restful_swagger_2 import Resource, swagger

from actinia_example_plugin.apidocs import helloworld
from actinia_example_plugin.core.example import transform_input
from actinia_example_plugin.model.response_models import (
    SimpleStatusCodeResponseModel,
)


class HelloWorld(Resource):
    """Returns 'Hello world!'."""

    def __init__(self) -> None:
        """Hello world class initialisation."""
        self.msg = "Hello world!"

    @swagger.doc(helloworld.describe_hello_world_get_docs)
    def get(self) -> SimpleStatusCodeResponseModel:
        """Get 'Hello world!' as answer string."""
        return SimpleStatusCodeResponseModel(status=200, message=self.msg)

    @swagger.doc(helloworld.describe_hello_world_post_docs)
    def post(self) -> SimpleStatusCodeResponseModel:
        """Hello World post method with name from postbody."""
        req_data = request.get_json(force=True)
        if isinstance(req_data, dict) is False or "name" not in req_data:
            return make_response("Missing name in JSON content", 400)
        name = req_data["name"]
        msg = f"{self.msg} {transform_input(name)}"

        return SimpleStatusCodeResponseModel(status=200, message=msg)
