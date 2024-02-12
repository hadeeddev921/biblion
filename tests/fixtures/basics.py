# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Common pytest fixtures for biblion."""

from datetime import UTC, datetime, timedelta

import pytest


@pytest.fixture(scope="module")
def yesterday():
    """Get yesterday timestamp."""
    return datetime.now(UTC) - timedelta(days=1)


@pytest.fixture(scope="module")
def tomorrow():
    """Get tomorrow timestamp."""
    return datetime.now(UTC) + timedelta(days=1)
