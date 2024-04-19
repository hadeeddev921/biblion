# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Budget resolver."""

import jsonresolver

from biblion.modules.jsonresolver import resolve_json_refs


@jsonresolver.route("/api/budgets/<pid>", host="bib.rero.ch")
def budget_resolver(pid):
    """Resolver for budget record."""
    return resolve_json_refs("budg", pid)
