# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Acquisition order line dumpers."""

from invenio_records.dumpers import Dumper as InvenioRecordsDumper

from biblion.modules.acquisition.acq_accounts.dumpers import AcqAccountGenericDumper
from biblion.modules.acquisition.acq_order_lines.models import AcqOrderLineNoteType
from biblion.modules.acquisition.dumpers import document_acquisition_dumper
from biblion.modules.commons.identifiers import IdentifierType
from biblion.modules.documents.extensions import TitleExtension


class AcqOrderLineESDumper(InvenioRecordsDumper):
    """ElasticSearch dumper class for an AcqOrderLine."""

    def dump(self, record, data):
        """Dump an AcqOrderLine instance for ElasticSearch.

        For ElasticSearch integration, we need to dump basic informations from
        a `AcqOrderLine` object instance, and add some data from related
        object : related account basic informations and related document basic
        informations.

        :param record: The record to dump.
        :param data: The initial dump data passed in by ``record.dumps()``.
        """
        # Keep only some attributes from AcqOrderLine object initial dump.
        for attr in ["pid", "status", "quantity"]:
            if value := record.get(attr):
                data.update({attr: value})

        # Add account information's: pid, name and reference number.
        # (remove None values from account metadata)
        account = record.account
        data["account"] = {
            "pid": account.pid,
            "name": account["name"],
            "number": account.get("number"),
        }
        data["account"] = {k: v for k, v in data["account"].items() if v}

        # Add document information's: pid, formatted title and ISBN
        # identifiers (remove None values from document metadata)
        if document := record.document:
            identifiers = document.get_identifiers(filters=[IdentifierType.ISBN], with_alternatives=True)
            identifiers = [identifier.normalize() for identifier in identifiers]
            data["document"] = {
                "pid": document.pid,
                "title": TitleExtension.format_text(document.get("title", [])),
                "identifiers": identifiers,
            }
            data["document"] = {k: v for k, v in data["document"].items() if v}
        else:
            # Document has been deleted; keep only the pid extracted from the $ref
            data["document"] = {"pid": record.document_pid, "type": "doc"}
        return data


class AcqOrderLineNotificationDumper(InvenioRecordsDumper):
    """Order line dumper class for acquisition order."""

    def dump(self, record, data):
        """Dump an AcqOrderLine instance for acquisition order notification.

        :param record: The record to dump.
        :param data: The initial dump data passed in by ``record.dumps()``.
        """
        # Dumps AcqOrderLine acquisition
        data.update(
            {
                "quantity": record.get("quantity"),
                "amount": record.get("amount"),
                "note": record.get_note(AcqOrderLineNoteType.VENDOR),
                "account": record.account.dumps(dumper=AcqAccountGenericDumper()),
                "document": record.document.dumps(dumper=document_acquisition_dumper),
            }
        )
        return {k: v for k, v in data.items() if v}
