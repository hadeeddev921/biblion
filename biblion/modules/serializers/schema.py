# SPDX-FileCopyrightText: Hadeed
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Biblion Record schema for serialization."""

from invenio_records_rest.schemas import RecordSchemaJSONV1 as _RecordSchemaJSONV1
from marshmallow import fields


class RecordSchemaJSONV1(_RecordSchemaJSONV1):
    """Schema for records Biblion in JSON.

    Add permissions & explanation fields.
    """

    permissions = fields.Raw()
    explanation = fields.Raw()
