# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Patron transactions serialization."""

from biblion.modules.libraries.api import LibrariesSearch
from biblion.modules.locations.api import LocationsSearch
from biblion.modules.patron_types.api import PatronTypesSearch
from biblion.modules.patrons.api import Patron
from biblion.modules.serializers import (
    CachedDataSerializerMixin,
    JSONSerializer,
    RecordSchemaJSONV1,
    search_responsify,
)


class PatronTransactionEventsJSONSerializer(JSONSerializer, CachedDataSerializerMixin):
    """Serializer for Biblion `PatronTransactionEvent` records as JSON."""

    def _postprocess_search_hit(self, hit):
        """Post-process each hit of a search result."""
        metadata = hit.get("metadata", {})

        # Add label for some $ref fields.
        pid = metadata.get("library", {}).get("pid")
        if pid and (resource := self.get_resource(LibrariesSearch(), pid)):
            metadata["library"]["name"] = resource.get("name")

        pid = metadata.get("patron_type", {}).get("pid")
        if pid and (resource := self.get_resource(PatronTypesSearch(), pid)):
            metadata["patron_type"]["name"] = resource.get("name")

        pid = metadata.get("operator", {}).get("pid")
        if pid and (resource := self.get_resource(Patron, pid)):
            metadata["operator"]["name"] = resource.formatted_name

        super()._postprocess_search_hit(hit)

    def _postprocess_search_aggregations(self, aggregations):
        """Post-process aggregations from a search result."""
        # enrich aggregation hit with some key
        aggrs = aggregations
        JSONSerializer.enrich_bucket_with_data(
            aggrs.get("transaction_library", {}).get("buckets", []),
            LibrariesSearch,
            "name",
        )
        JSONSerializer.enrich_bucket_with_data(
            aggrs.get("patron_type", {}).get("buckets", []), PatronTypesSearch, "name"
        )
        JSONSerializer.enrich_bucket_with_data(
            aggrs.get("owning_library", {}).get("buckets", []), LibrariesSearch, "name"
        )
        for loc_bucket in aggrs.get("owning_library", {}).get("buckets", []):
            JSONSerializer.enrich_bucket_with_data(
                loc_bucket.get("owning_location", {}).get("buckets", []),
                LocationsSearch,
                "name",
            )

        # add configuration for date-range facets
        aggr = aggregations.get("transaction_date", {})
        JSONSerializer.add_date_range_configuration(aggr)

        super()._postprocess_search_aggregations(aggregations)


_json = PatronTransactionEventsJSONSerializer(RecordSchemaJSONV1)
json_ptre_search = search_responsify(_json, "application/rero+json")
