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

Hello World test
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


import json

import pytest
from actinia_api import URL_PREFIX
from flask import Response

from tests.testsuite import ActiniaTestCase

STATUS_CODE_200 = 200
STATUS_CODE_400 = 400
STATUS_CODE_404 = 404


class ActiniaHelloWorldTest(ActiniaTestCase):
    """Actinia hello world test class for hello world endpoint."""

    @pytest.mark.integrationtest
    def test_get_helloworld(self) -> None:
        """Test get method of /helloworld/projects/<project_name> endpoint."""
        resp = self.app.get(
            f"{URL_PREFIX}/helloworld/{self.project_url_part}/project1",
        )

        assert isinstance(
            resp,
            Response,
        ), "The response is not of type Response"
        assert (
            resp.status_code == STATUS_CODE_200
        ), f"The status code is not {STATUS_CODE_200}"
        assert hasattr(resp, "json"), "The response has no attribute 'json'"
        assert (
            "message" in resp.json
        ), "There is no 'message' inside the response"
        assert (
            resp.json["message"] == "Project: Hello world! project1"
        ), "The response message is wrong"

    @pytest.mark.integrationtest
    def test_post_helloworld(self) -> None:
        """Test post method of /helloworld/projects/<project_name> endpoint."""
        postbody = {"name": "test"}
        resp = self.app.post(
            f"{URL_PREFIX}/helloworld/{self.project_url_part}/project1",
            headers=self.user_auth_header,
            data=json.dumps(postbody),
            content_type="application/json",
        )
        assert isinstance(
            resp,
            Response,
        ), "The response is not of type Response"
        assert (
            resp.status_code == STATUS_CODE_200
        ), f"The status code is not {STATUS_CODE_200}"
        assert hasattr(resp, "json"), "The response has no attribute 'json'"
        assert (
            "message" in resp.json
        ), "There is no 'message' inside the response"
        assert (
            resp.json["message"] == ("Project: Hello world!"
                                     " Hello world TEST! project1")
        ), "The response message is wrong"

    @pytest.mark.integrationtest
    def test_post_helloworld_error(self) -> None:
        """Test post method of /helloworld/projects/<project_name> endpoint."""
        postbody = {"namee": "test"}
        resp = self.app.post(
            f"{URL_PREFIX}/helloworld/{self.project_url_part}/project1",
            headers=self.user_auth_header,
            data=json.dumps(postbody),
            content_type="application/json",
        )
        assert isinstance(
            resp,
            Response,
        ), "The response is not of type Response"
        assert (
            resp.status_code == STATUS_CODE_400
        ), f"The status code is not {STATUS_CODE_400}"
        assert resp.data == b"Missing name in JSON content"

    @pytest.mark.integrationtest
    def test_redirecting_deprecated_locations_endpoint(self) -> None:
        """Test redirecting of deprecated locations to projects endpoint."""
        if self.grass_version >= [8, 4]:
            resp = self.app.get(
                f"{URL_PREFIX}/helloworld/locations/project1",
            )
            assert isinstance(
                resp,
                Response,
            ), "The response is not of type Response"
            assert (
                resp.status_code == STATUS_CODE_200
            ), f"The status code is not {STATUS_CODE_200}"
            resp_location = resp.location.replace("http://localhost", "")
            assert (
                resp_location == f"{URL_PREFIX}/helloworld/projects/project1"
            ), ("The deprecated locations endpoint "
                "is not forwarded to projects endpoint")

    @pytest.mark.integrationtest
    def test_projects_endpoint_for_lt_g84(self) -> None:
        """Test non-supported project endpoint for GRASS versions < g84"""
        if self.grass_version < [8, 4]:
            resp = self.app.get(
                f"{URL_PREFIX}/helloworld/projects/project1",
            )
            assert isinstance(
                resp,
                Response,
            ), "The response is not of type Response"
            assert (
                resp.status_code == STATUS_CODE_404
            ), f"The status code is not {STATUS_CODE_404}"
            assert (
                resp.json["message"] == (
                                         "Not Found. The requested URL "
                                         "is only available from "
                                         "GRASS GIS version 8.4."
                                         )
            ), f"Wrong return message: {resp.data}"
