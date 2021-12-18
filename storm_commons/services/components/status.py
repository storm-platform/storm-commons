# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.services.records.components import ServiceComponent


class SoftDeleteComponent(ServiceComponent):
    """Service component which set the user context in the record."""

    def delete(self, identity, data=None, record=None, **kwargs):
        """Create handler."""
        record.is_deleted = True


class FinishStatusComponent(ServiceComponent):
    """Service component which set the record status (``is_finished``)."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Create handler."""
        record.is_finished = False

    def finish(self, identity, data=None, record=None, **kwargs):
        """Finish status handler"""
        if record:
            record.is_finished = True
