# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import re

from marshmallow import ValidationError
from invenio_pidstore.errors import PIDAlreadyExists

from invenio_records_resources.services.records.components import ServiceComponent


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
        """Create a Record PID from its metadata."""

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
