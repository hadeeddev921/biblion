# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Acquisition order serialization."""

from biblion.modules.acquisition.acq_accounts.api import AcqAccountsSearch
from biblion.modules.acquisition.budgets.api import BudgetsSearch
from biblion.modules.libraries.api import LibrariesSearch
from biblion.modules.serializers import ACQJSONSerializer, JSONSerializer
from biblion.modules.vendors.api import VendorsSearch


class AcqOrderJSONSerializer(ACQJSONSerializer):
    """Mixin serializing records as JSON."""

    def _postprocess_search_aggregations(self, aggregations):
        """Post-process aggregations from a search result."""
        JSONSerializer.enrich_bucket_with_data(
            aggregations.get("library", {}).get("buckets", []), LibrariesSearch, "name"
        )
        JSONSerializer.enrich_bucket_with_data(aggregations.get("vendor", {}).get("buckets", []), VendorsSearch, "name")
        JSONSerializer.enrich_bucket_with_data(
            aggregations.get("account", {}).get("buckets", []),
            AcqAccountsSearch,
            "name",
        )
        JSONSerializer.enrich_bucket_with_data(aggregations.get("budget", {}).get("buckets", []), BudgetsSearch, "name")
        # Add configuration for order_date and receipt_date buckets
        for aggr_name in ["order_date", "receipt_date"]:
            aggr = aggregations.get(aggr_name, {})
            JSONSerializer.add_date_range_configuration(aggr)

        super()._postprocess_search_aggregations(aggregations)
