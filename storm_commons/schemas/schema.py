# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from marshmallow import fields, Schema


class Agent(Schema):
    """An agent schema.

    Note:
        This code is adapted from: https://github.com/inveniosoftware/invenio-rdm-records/blob/d7e7c7a2a44986de88e2d7941722bc72fd7dc345/invenio_rdm_records/services/schemas/parent/access.py#L42
    """

    user = fields.Integer(required=False)

    project = fields.Integer(required=False)
