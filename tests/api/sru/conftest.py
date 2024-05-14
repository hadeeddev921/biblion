# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""SRU test fixtures."""

import pytest


@pytest.fixture()
def sru_result_set_client(client):
    """Yield a client with BIBLION_SRU_RESULT_SET_TTL set to 60 seconds."""
    client.application.config["BIBLION_SRU_RESULT_SET_TTL"] = 60
    yield client
    client.application.config.pop("BIBLION_SRU_RESULT_SET_TTL", None)
