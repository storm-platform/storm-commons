# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_project.proxies import current_project
from invenio_records_resources.services.records.components import ServiceComponent


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


__all__ = ("ProjectComponent", "PipelineComponent", "UserComponent")
