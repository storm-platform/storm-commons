# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from copy import copy

from invenio_records_resources.services.records.components import ServiceComponent


class RecordMetadataComponent(ServiceComponent):
    """Service component for metadata.

    Note:
        (class-vendoring) Imported class from Invenio RDM Records to reduce dependencies in the system.
        (https://github.com/inveniosoftware/invenio-rdm-records/blob/d7e7c7a2a44986de88e2d7941722bc72fd7dc345/invenio_rdm_records/services/components/metadata.py#L18)
    """

    new_version_skip_fields = []

    def create(self, identity, data=None, record=None, **kwargs):
        """Inject parsed metadata to the record."""
        record.metadata = data.get("metadata", {})

    def update(self, identity, data=None, record=None, **kwargs):
        """Update handler."""
        record.metadata = data.get("metadata", {})

    def update_draft(self, identity, data=None, record=None, **kwargs):
        """Inject parsed metadata to the record."""
        record.metadata = data.get("metadata", {})

    def publish(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        record.metadata = draft.get("metadata", {})

    def edit(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        draft.metadata = record.get("metadata", {})

    def new_version(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        draft.metadata = copy(record.get("metadata", {}))
        # Remove fields that should not be copied to the new version
        # (publication date and version)
        for f in self.new_version_skip_fields:
            draft.metadata.pop(f, None)
