# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Biblion Unified entities serialization."""

from biblion.modules.serializers import RecordSchemaJSONV1, search_responsify

from .base import EntityJSONSerializer

# Serializers
# ===========
_json = EntityJSONSerializer(RecordSchemaJSONV1)

# Records-REST serializers
# ========================
json_entities_search = search_responsify(_json, "application/json")
