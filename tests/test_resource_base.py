#!/usr/bin/env python
"""SPDX-FileCopyrightText: (c) 2016-2022 by mundialis GmbH & Co. KG.

SPDX-License-Identifier: GPL-3.0-or-later

Tests: Actinia resource test case base
"""

from __future__ import annotations

import atexit
import base64
import os
import signal
import tempfile
import time
from pathlib import Path

from actinia_core.core.common.config import global_config
from actinia_core.core.common.user import ActiniaUser
from actinia_core.endpoints import create_endpoints
from actinia_core.testsuite import ActiniaTestCaseBase
from werkzeug.datastructures import Headers

__license__ = "GPL-3.0-or-later"
__author__ = "Sören Gebbert, Anika Weinmann"
__copyright__ = (
    "Copyright 2016-2022, Sören Gebbert and mundialis GmbH & Co. KG"
)
__maintainer__ = "mundialis GmbH & Co. KG"

# Create endpoints
create_endpoints()

KVDB_PID = None
SERVER_TEST = False
CUSTOM_ACTINIA_CFG = False

# If this environmental variable is set, then a real http request will be send
# instead of using the flask test_client.
if "ACTINIA_SERVER_TEST" in os.environ:
    SERVER_TEST = bool(os.environ["ACTINIA_SERVER_TEST"])
# Set this variable to use a actinia config file in a docker container
if "ACTINIA_CUSTOM_TEST_CFG" in os.environ:
    CUSTOM_ACTINIA_CFG = str(os.environ["ACTINIA_CUSTOM_TEST_CFG"])


def setup_environment() -> None:
    """Setuo test environment."""
    global KVDB_PID
    # Set the port to the test kvdb server
    global_config.KVDB_SERVER_SERVER = "localhost"
    global_config.KVDB_SERVER_PORT = 7000
    # Set the path to kvdb WORKER_LOGFILE
    # global_config.WORKER_LOGFILE = "/var/log/kvdb/kvdb"

    # home = os.getenv("HOME")

    # GRASS GIS
    # Setup the test environment
    global_config.GRASS_GIS_BASE = "/usr/local/grass/"
    global_config.GRASS_GIS_START_SCRIPT = "/usr/local/bin/grass"
    # global_config.GRASS_DATABASE= "/usr/local/grass_test_db"
    # global_config.GRASS_DATABASE = "%s/actinia/grass_test_db" % home
    global_config.GRASS_TMP_DATABASE = tempfile.TemporaryDirectory().name
    Path(global_config.GRASS_TMP_DATABASE).mkdir(parents=True)

    if SERVER_TEST is False and CUSTOM_ACTINIA_CFG is False:
        # Start the kvdb server for user and logging management
        KVDB_PID = os.spawnl(
            os.P_NOWAIT,
            "/usr/bin/valkey-server",
            "common/valkey.conf",
            f"--port {global_config.KVDB_SERVER_PORT}",
        )
        time.sleep(1)

    if SERVER_TEST is False and CUSTOM_ACTINIA_CFG is not False:
        global_config.read(CUSTOM_ACTINIA_CFG)


def stop_kvdb() -> None:
    """Stop kvdb server."""
    # Kill th kvdb server
    if SERVER_TEST is False and KVDB_PID is not None:
        os.kill(KVDB_PID, signal.SIGTERM)


# Register the kvdb stop function
atexit.register(stop_kvdb)
# Setup the environment
setup_environment()


class ActiniaResourceTestCaseBase(ActiniaTestCaseBase):
    """Actinia resource test case base class."""

    @classmethod
    def create_user(
        cls,
        name: str = "guest",
        role: str = "guest",
        group: str = "group",
        password: str = "abcdefgh",
        accessible_datasets: dict[str, list | None] | None = None,
        process_num_limit: int = 1000,
        process_time_limit: int = 6000,
        accessible_modules: list[str] | None = None,
    ) -> (str, str, Headers()):
        """Create actinia user."""
        auth = bytes(f"{name}:{password}", "utf-8")

        # We need to create an HTML basic authorization header
        cls.auth_header[role] = Headers()
        cls.auth_header[role].add(
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
            process_num_limit=process_num_limit,
            process_time_limit=process_time_limit,
        )
        if accessible_modules is None:
            accessible_modules = ["sleep"]
        user.add_accessible_modules(accessible_modules)
        user.update()
        cls.users_list.append(user)

        return name, group, cls.auth_header[role]
