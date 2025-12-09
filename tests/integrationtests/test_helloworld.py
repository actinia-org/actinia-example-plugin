#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2022 by mundialis GmbH & Co. KG.

SPDX-License-Identifier: GPL-3.0-or-later

Hello World test
"""

__license__ = "GPL-3.0-or-later"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


import json

import pytest
from actinia_api import URL_PREFIX
from flask import Response

from tests.testsuite import ActiniaTestCase


class ActiniaHelloWorldTest(ActiniaTestCase):
    """Actinia hello world test class for hello world endpoint."""

    @pytest.mark.integrationtest
    def test_get_helloworld(self) -> None:
        """Test the get method of the /helloworld endpoint."""
        resp = self.app.get(f"{URL_PREFIX}/helloworld")

        assert isinstance(
            resp,
            Response,
        ), "The response is not of type Response"
        assert resp.status_code == 200, "The status code is not 200"
        assert hasattr(resp, "json"), "The response has no attribute 'json'"
        assert (
            "message" in resp.json
        ), "There is no 'message' inside the response"
        assert (
            resp.json["message"] == "Hello world!"
        ), "The response message is wrong"

    @pytest.mark.integrationtest
    def test_post_helloworld(self) -> None:
        """Test the post method of the /helloworld endpoint."""
        postbody = {"name": "test"}
        resp = self.app.post(
            f"{URL_PREFIX}/helloworld",
            headers=self.user_auth_header,
            data=json.dumps(postbody),
            content_type="application/json",
        )
        assert isinstance(
            resp,
            Response,
        ), "The response is not of type Response"
        assert resp.status_code == 200, "The status code is not 200"
        assert hasattr(resp, "json"), "The response has no attribute 'json'"
        assert (
            "message" in resp.json
        ), "There is no 'message' inside the response"
        assert (
            resp.json["message"] == "Hello world! Hello world TEST!"
        ), "The response message is wrong"

    @pytest.mark.integrationtest
    def test_post_helloworld_error(self) -> None:
        """Test the post method of the /helloworld endpoint."""
        postbody = {"namee": "test"}
        resp = self.app.post(
            f"{URL_PREFIX}/helloworld",
            headers=self.user_auth_header,
            data=json.dumps(postbody),
            content_type="application/json",
        )
        assert isinstance(
            resp,
            Response,
        ), "The response is not of type Response"
        assert resp.status_code == 400, "The status code is not 400"
        assert resp.data == b"Missing name in JSON content"
