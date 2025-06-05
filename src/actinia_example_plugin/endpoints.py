#!/usr/bin/env python
"""Copyright (c) 2018-2025 mundialis GmbH & Co. KG.

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

from flask_restful_swagger_2 import Api, Resource

from actinia_example_plugin.api.helloworld import HelloWorld
from actinia_example_plugin.api.project_helloworld import ProjectHelloWorld


def get_endpoint_class_name(
    endpoint_class: Resource,
    projects_url_part: str = "projects",
) -> str:
    """Create the name for the given endpoint class."""
    endpoint_class_name = endpoint_class.__name__.lower()
    if projects_url_part != "projects":
        name = f"{endpoint_class_name}_{projects_url_part}"
    else:
        name = endpoint_class_name
    return name


def create_project_endpoints(
    apidoc: Api,
    projects_url_part: str = "projects",
) -> None:
    """Add resources with "project" inside the endpoint url to the api.

    Args:
        apidoc (Api): Flask api
        projects_url_part (str): The name of the projects inside the endpoint
                                 URL; to add deprecated location endpoints set
                                 it to "locations"

    """
    apidoc.add_resource(
        ProjectHelloWorld,
        f"/helloworld/{projects_url_part}/<string:project_name>",
        endpoint=get_endpoint_class_name(ProjectHelloWorld, projects_url_part),
    )


# endpoints loaded if run as actinia-core plugin as well as standalone app
def create_endpoints(flask_api: Api) -> None:
    """Create plugin endpoints."""
    apidoc = flask_api

    apidoc.add_resource(HelloWorld, "/helloworld")

    # add deprecated location endpoints
    create_project_endpoints(apidoc, projects_url_part="locations")

    # add project endpoints
    create_project_endpoints(apidoc, projects_url_part="projects")
