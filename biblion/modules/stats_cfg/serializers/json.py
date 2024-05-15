# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Statistics configuration serialization."""

from biblion.modules.libraries.api import LibrariesSearch
from biblion.modules.serializers import JSONSerializer
from biblion.modules.serializers.mixins import PostprocessorMixin


class StatsCfgJSONSerializer(JSONSerializer, PostprocessorMixin):
    """Mixin serializing records as JSON."""

    def _postprocess_search_aggregations(self, aggregations):
        """Post-process aggregations from a search result.

        :param aggregations: the dictionary representing ElasticSearch
                            aggregations section.
        """
        JSONSerializer.enrich_bucket_with_data(
            aggregations.get("library", {}).get("buckets", []), LibrariesSearch, "name"
        )

        super()._postprocess_search_aggregations(aggregations)
