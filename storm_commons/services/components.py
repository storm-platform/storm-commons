# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import re

from marshmallow import ValidationError
from invenio_pidstore.errors import PIDAlreadyExists

from storm_project.proxies import current_project

from invenio_access.permissions import system_process
from invenio_records_resources.services.records.components import ServiceComponent

from invenio_records.dictutils import dict_set


class ProjectComponent(ServiceComponent):
    """Service component which set the project context in the record."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create handler."""
        record.project_id = current_project._obj.model.id


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


class BaseAccessComponent(ServiceComponent):
    """Base component to define record access.

    See:
        This code is adapted from: https://github.com/inveniosoftware/invenio-communities/blob/837f33f1c0013a69fcec0ef188200a99fafddc47/invenio_communities/communities/services/components.py#L126
    """

    def _populate_access(self, identity, data, record, **kwargs):
        if record is not None and "access" in data:
            record.setdefault("access", {})
            record["access"].update(data.get("access", {}))

    def _init_access_entities(self, identity, record, access_field, **kwargs):
        """Initialize the access fields."""
        is_system_process = system_process in identity.provides

        initial_entities = [{"user": identity.id}] if not is_system_process else []
        dict_set(record, access_field, initial_entities)

    def create(self, identity, data=None, record=None, **kwargs):
        """Add basic ownership fields to the record."""

        self._populate_access(identity, data, record, **kwargs)

        self._init_access_entities(identity, record, "access.owned_by", **kwargs)
        self._init_access_entities(identity, record, "access.contributed_by", **kwargs)

    def update(self, identity, data=None, record=None, **kwargs):
        """Update handler."""
        self._populate_access(identity, data, record, **kwargs)

    def update_draft(self, identity, data=None, record=None, **kwargs):
        """Update handler."""
        self._populate_access(identity, data, record, **kwargs)

    def publish(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        record.access = draft.access

    def edit(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        draft.access = record.access

    def new_version(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        draft.access = record.access


__all__ = (
    "BaseAccessComponent",
    "CustomPIDGeneratorComponent",
    "RecordServiceTypeComponent",
    "ProjectComponent",
    "UserComponent",
)
