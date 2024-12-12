#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

Add endpoints to flask app with endpoint definitions and routes
"""

__license__ = "GPLv3"
__author__ = "Carmen Tawalika, Anika Weinmann"
__copyright__ = "Copyright 2022-2024 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"

from actinia_core.endpoints import get_endpoint_class_name

from actinia_example_plugin.api.helloworld import HelloWorld
from actinia_example_plugin.api.project_helloworld import ProjectHelloWorld


def create_project_endpoints(apidoc, projects_url_part="projects") -> None:
    """
    Function to add resources with "project" inside the endpoint url.

    Args:
        apidoc (flask_restful_swagger_2.Api): Flask api
        projects_url_part (str): The name of the projects inside the endpoint
                                 URL; to add deprecated location endpoints set
                                 it to "locations"
    """

    apidoc.add_resource(
        ProjectHelloWorld,
        "<string:project_name>/helloworld",
        endpoint=get_endpoint_class_name(ProjectHelloWorld, projects_url_part),
    )


# endpoints loaded if run as actinia-core plugin as well as standalone app
def create_endpoints(flask_api) -> None:
    """Create plugin endpoints."""
    apidoc = flask_api

    apidoc.add_resource(HelloWorld, "/helloworld")

    # add deprecated location endpoints
    create_project_endpoints(apidoc, projects_url_part="locations")

    # add project endpoints
    create_project_endpoints(apidoc, projects_url_part="projects")
