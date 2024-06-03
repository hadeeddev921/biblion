# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Test permissions."""

from biblion.modules.permissions import has_superuser_access
from biblion.permissions import librarian_update_permission_factory
from tests.utils import login_user_for_view


def test_has_superuser_access(app):
    """Test permissions of has_superuser_access functions."""
    assert not has_superuser_access()
    app.config["BIBLION_DISABLE_PERMISSION_CHECKS"] = True
    assert has_superuser_access()


def test_librarian_update_permission_factory(client, document, ebook_1, librarian_martigny, default_user_password):
    """Test librarian_update_permission_factory function."""
    assert not librarian_update_permission_factory(ebook_1).can()
    login_user_for_view(client, librarian_martigny, default_user_password)
    assert librarian_update_permission_factory(document).can()
