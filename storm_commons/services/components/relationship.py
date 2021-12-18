# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.services.records.components import ServiceComponent


class UserComponent(ServiceComponent):
    """Service component which set the user context in the record."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create handler."""
        record.user_id = identity.id


class RecordServiceComponent(ServiceComponent):
    """Service component which set the service context in the record."""

    def create(self, identity, data=None, record=None, service=None, **kwargs):
        """Create handler."""
        record.service = service or data.get("service")
