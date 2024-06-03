# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Test explain."""

from biblion.modules.sru.explain import Explain


def test_explain(app):
    """Test Explain."""
    explain = Explain("api/sru")
    explain_strings = str(explain).split("\n")
    assert explain_strings[0] == '<sru:explainResponse xmlns:sru="http://www.loc.gov/standards/sru/">'
    assert explain.database == "api/sru"
    assert explain.number_of_records == app.config.get("BIBLION_SRU_NUMBER_OF_RECORDS")
    assert explain.maximum_records == app.config.get("BIBLION_SRU_MAXIMUM_RECORDS")
    assert explain.doc_type == "doc"
    assert explain.index == app.config.get("RECORDS_REST_ENDPOINTS", {}).get("doc", {}).get("search_index")
