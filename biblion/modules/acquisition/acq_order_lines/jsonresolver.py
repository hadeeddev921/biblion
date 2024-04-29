# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Acquisition Order Line resolver."""

import jsonresolver

from biblion.modules.jsonresolver import resolve_json_refs


@jsonresolver.route("/api/acq_order_lines/<pid>", host="bib.rero.ch")
def acq_order_line_resolver(pid):
    """Resolver for Acquisition Order Line record."""
    return resolve_json_refs("acol", pid)
