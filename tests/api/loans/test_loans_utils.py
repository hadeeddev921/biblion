# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Tests loans utils."""

from biblion.modules.items.utils import item_pid_to_object
from biblion.modules.loans.api import Loan
from biblion.modules.loans.utils import (
    loan_build_document_ref,
    loan_build_item_ref,
    loan_build_patron_ref,
)
from biblion.modules.utils import get_ref_for_pid


def test_loans_build_refs(item_lib_martigny, patron_martigny, document):
    """Test functions buildings refs."""
    # Create "virtual" Loan (not registered)
    loan = Loan(
        {
            "item_pid": item_pid_to_object(item_lib_martigny.pid),
            "document_pid": document.pid,
            "patron_pid": patron_martigny.pid,
        }
    )

    assert loan_build_item_ref(None, loan) == get_ref_for_pid("items", item_lib_martigny.pid)
    assert loan_build_document_ref(None, loan) == get_ref_for_pid("doc", document.pid)
    assert loan_build_patron_ref(None, loan) == get_ref_for_pid("patrons", patron_martigny.pid)
