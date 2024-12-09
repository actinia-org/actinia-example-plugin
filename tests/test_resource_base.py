#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2016-2022 mundialis GmbH & Co. KG

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

Tests: Actinia resource test case base
"""

import atexit
import base64
import os
import signal
import time

from werkzeug.datastructures import Headers

from actinia_core.testsuite import ActiniaTestCaseBase, URL_PREFIX
from actinia_core.core.common.user import ActiniaUser
from actinia_core.core.common.config import global_config
from actinia_core.endpoints import create_endpoints


__license__ = "GPLv3"
__author__ = "Sören Gebbert, Anika Weinmann"
__copyright__ = (
    "Copyright 2016-2022, Sören Gebbert and mundialis GmbH & Co. KG"
)
__maintainer__ = "mundialis GmbH & Co. KG"

# Create endpoints
create_endpoints()

REDIS_PID = None
SERVER_TEST = False
CUSTOM_ACTINIA_CFG = False

# If this environmental variable is set, then a real http request will be send
# instead of using the flask test_client.
if "ACTINIA_SERVER_TEST" in os.environ:
    SERVER_TEST = bool(os.environ["ACTINIA_SERVER_TEST"])
# Set this variable to use a actinia config file in a docker container
if "ACTINIA_CUSTOM_TEST_CFG" in os.environ:
    CUSTOM_ACTINIA_CFG = str(os.environ["ACTINIA_CUSTOM_TEST_CFG"])


def setup_environment():
    """Setuo test environment"""

    global REDIS_PID
    # Set the port to the test redis server
    global_config.REDIS_SERVER_SERVER = "localhost"
    global_config.REDIS_SERVER_PORT = 7000
    # Set the path to redis WORKER_LOGFILE
    # global_config.WORKER_LOGFILE = "/var/log/redis/redis"

    # home = os.getenv("HOME")

    # GRASS GIS
    # Setup the test environment
    global_config.GRASS_GIS_BASE = "/usr/local/grass/"
    global_config.GRASS_GIS_START_SCRIPT = "/usr/local/bin/grass"
    # global_config.GRASS_DATABASE= "/usr/local/grass_test_db"
    # global_config.GRASS_DATABASE = "%s/actinia/grass_test_db" % home
    global_config.GRASS_TMP_DATABASE = "/tmp"

    if SERVER_TEST is False and CUSTOM_ACTINIA_CFG is False:
        # Start the redis server for user and logging management
        REDIS_PID = os.spawnl(
            os.P_NOWAIT,
            "/usr/bin/redis-server",
            "common/redis.conf",
            f"--port {global_config.REDIS_SERVER_PORT}",
        )
        time.sleep(1)

    if SERVER_TEST is False and CUSTOM_ACTINIA_CFG is not False:
        global_config.read(CUSTOM_ACTINIA_CFG)


def stop_redis():
    """Function to stop redis"""
    if SERVER_TEST is False:
        global REDIS_PID
        # Kill th redis server
        if REDIS_PID is not None:
            os.kill(REDIS_PID, signal.SIGTERM)


# Register the redis stop function
atexit.register(stop_redis)
# Setup the environment
setup_environment()


class ActiniaResourceTestCaseBase(ActiniaTestCaseBase):
    """Actinia resource test case base class"""

    @classmethod
    def create_user(
        cls,
        name="guest",
        role="guest",
        group="group",
        password="abcdefgh",
        accessible_datasets=None,
        process_num_limit=1000,
        process_time_limit=6000,
        accessible_modules=None,
    ):
        """Create actinia user"""
        auth = bytes(f"{name}:{password}", "utf-8")

        # We need to create an HTML basic authorization header
        cls.auth_header[role] = Headers()
        cls.auth_header[role].add(
            "Authorization", "Basic " + base64.b64encode(auth).decode()
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
