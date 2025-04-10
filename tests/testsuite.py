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

Base class for GRASS GIS REST API tests
"""

from __future__ import annotations

__license__ = "GPLv3"
__author__ = "Carmen Tawalika, Sören Gebbert"
__copyright__ = "Copyright 2018-2022 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"

import base64
import unittest
from typing import ClassVar

import pwgen
from actinia_core.core.common import kvdb_interface
from actinia_core.core.common.app import flask_app
from actinia_core.core.common.config import global_config
from actinia_core.core.common.user import ActiniaUser
from actinia_core.version import G_VERSION, init_versions
from werkzeug.datastructures import Headers


class ActiniaTestCase(unittest.TestCase):
    """Actinia test case class."""

    # guest = None
    # admin = None
    # superadmin = None
    user: str = None
    auth_header: ClassVar[dict] = {}
    users_list: ClassVar[list[str]] = []
    project_url_part: str = "projects"

    # set project_url_part to "locations" if GRASS GIS version < 8.4
    init_versions()

    grass_version_s: str = G_VERSION["version"]
    grass_version: ClassVar[list[int]] = [
        int(item) for item in grass_version_s.split(".")[:2]
    ]
    if grass_version < [8, 4]:
        project_url_part = "locations"

    def setUp(self) -> None:
        """Overwrite method setUp from unittest.TestCase class."""
        self.app_context = flask_app.app_context()
        self.app_context.push()
        # from http://flask.pocoo.org/docs/0.12/api/#flask.Flask.test_client:
        # Note that if you are testing for assertions or exceptions in your
        # application code, you must set app.testing = True in order for the
        # exceptions to propagate to the test client.  Otherwise, the exception
        # will be handled by the application (not visible to the test client)
        # and the only indication of an AssertionError or other exception will
        # be a 500 status code response to the test client.
        flask_app.testing = True
        self.app = flask_app.test_client()

        # Start and connect the kvdb interface
        kvdb_args = (
            global_config.KVDB_SERVER_URL,
            global_config.KVDB_SERVER_PORT,
        )
        if (
            global_config.KVDB_SERVER_PW
            and global_config.KVDB_SERVER_PW is not None
        ):
            kvdb_args = (*kvdb_args, global_config.KVDB_SERVER_PW)
        kvdb_interface.connect(*kvdb_args)

        # create test user for roles user (more to come)
        accessible_datasets = {
            "nc_spm_08": ["PERMANENT", "user1", "modis_lst"],
        }
        password = pwgen.pwgen()
        (
            self.user_id,
            self.user_group,
            self.user_auth_header,
        ) = self.create_user(
            name="user",
            role="user",
            password=password,
            process_num_limit=3,
            process_time_limit=4,
            accessible_datasets=accessible_datasets,
        )
        (
            self.restricted_user_id,
            self.restricuted_user_group,
            self.restricted_user_auth_header,
        ) = self.create_user(
            name="user2",
            role="user",
            password=password,
            process_num_limit=3,
            process_time_limit=4,
            accessible_datasets=accessible_datasets,
            accessible_modules=["v.db.select", "importer", "r.mapcalc"],
        )
        (
            self.admin_id,
            self.admin_group,
            self.admin_auth_header,
        ) = self.create_user(
            name="admin",
            role="admin",
            password=password,
            process_num_limit=3,
            process_time_limit=4,
            accessible_datasets=accessible_datasets,
        )

        # # create process queue
        # from actinia_core.core.common.process_queue import \
        #    create_process_queue
        # create_process_queue(config=global_config)

    def tearDown(self) -> None:
        """Overwrite method tearDown from unittest.TestCase class."""
        self.app_context.pop()

        # remove test user; disconnect kvdb
        for user in self.users_list:
            user.delete()
        kvdb_interface.disconnect()

    def create_user(
        self,
        name: str = "guest",
        role: str = "guest",
        group: str = "group",
        password: str = "abcdefgh",
        accessible_datasets: dict[str, list | None] | None = None,
        process_num_limit: int = 1000,
        process_time_limit: int = 6000,
        accessible_modules: list[str] = global_config.MODULE_ALLOW_LIST,
    ) -> (str, str, Headers()):
        """Create actinia user."""
        auth = bytes(f"{name}:{password}", "utf-8")
        # We need to create an HTML basic authorization header
        self.auth_header[role] = Headers()
        self.auth_header[role].add(
            "Authorization",
            f"Basic {base64.b64encode(auth).decode()}",
        )

        # Make sure the user database is empty
        user = ActiniaUser(name)
        if user.exists():
            user.delete()
        # Create a user in the database
        user = ActiniaUser.create_user(
            name,
            group,
            password,
            user_role=role,
            accessible_datasets=accessible_datasets,
            accessible_modules=accessible_modules,
            process_num_limit=process_num_limit,
            process_time_limit=process_time_limit,
        )
        user.add_accessible_modules(["uname", "sleep"])
        self.users_list.append(user)

        return name, group, self.auth_header[role]


# def check_started_process(test_case: , resp: ) -> None:
#     """Checks response of started process - TODO: can be enhanced."""
#     if isinstance(resp.json["process_results"], dict):
#         resp.json["process_results"] = str(resp.json["process_results"])
#     resp_class = ProcessingResponseModel(**resp.json)
#     assert resp_class["status"] == "accepted"
#     status_url = resp_class["urls"]["status"]

#     # poll status_url
#     # TODO: status stays in accepted
#     status_resp = test_case.app.get(
#         status_url,
#         headers=test_case.user_auth_header,
#     )
#     assert status_resp.json["urls"]["status"] == status_url
