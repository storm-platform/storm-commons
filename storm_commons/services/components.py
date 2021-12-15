# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import re

from marshmallow import ValidationError
from invenio_pidstore.errors import PIDAlreadyExists

from invenio_access.permissions import system_process
from invenio_records_resources.services.records.components import ServiceComponent

from invenio_records.dictutils import dict_set


class UserComponent(ServiceComponent):
    """Service component which set the user context in the record."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create handler."""
        record.user_id = identity.id


class RecordServiceTypeComponent(ServiceComponent):
    """Service component which set the service context in the record."""

    def create(self, identity, data=None, record=None, service=None, **kwargs):
        """Create handler."""
        record.service = service or data.get("service")


class CustomPIDGeneratorComponent(ServiceComponent):
    """Component to create unique and customized PIDs.

    See:
        This class is adapted from: https://github.com/inveniosoftware/invenio-communities/blob/837f33f1c0013a69fcec0ef188200a99fafddc47/invenio_communities/communities/services/components.py#L18
    """

    @classmethod
    def _validate(cls, pid_value):
        """Checks the validity of the provided pid value."""

        blop = re.compile("^[-\w]+$")

        if not bool(blop.match(pid_value)):
            raise ValidationError(
                "The ID should contain only letters with numbers or dashes.",
                field_name="id",
            )

    def create(self, identity, record=None, data=None, **kwargs):
        """Create a Research Project PID from its metadata."""

        data["id"] = data["id"].lower()
        self._validate(data["id"])
        record["id"] = data["id"]

        try:
            provider = record.__class__.pid.field._provider.create(record=record)
        except PIDAlreadyExists:
            raise ValidationError(
                "The selected identifier already exists.", field_name="id"
            )
        setattr(record, "pid", provider.pid)


class VersionedRecordAccessDefinitionComponent(ServiceComponent):
    """Access component to versioned records with parent."""

    def _create(self, identity, data=None, record=None, **kwargs):
        """Extra ``create`` method operation."""
        pass

    def create(self, identity, data=None, record=None, **kwargs):
        """Add basic ownership fields to the record."""

        parent = record.parent
        if parent:
            parent.access.contributors.append({"user": identity.id})

            # extra method: this method was added to users provides
            # arbitrary functions for the ``create`` operation.
            self._create(identity, data, record, **kwargs)


class RecordAccessDefinitionComponent(ServiceComponent):
    """Access component to versioned records without parent."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Add basic ownership fields to the record."""
        if record:
            _user_obj = {"user": identity.id}

            record.access.owners.append(_user_obj)
            record.access.contributors.append(_user_obj)


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


__all__ = (
    "CustomPIDGeneratorComponent",
    "RecordServiceTypeComponent",
    "UserComponent",
    "RecordMetadataComponent",
    "VersionedRecordAccessDefinitionComponent",
    "RecordAccessDefinitionComponent",
)
