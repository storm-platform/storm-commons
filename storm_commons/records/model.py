# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import uuid
from datetime import datetime

from invenio_db import db
from sqlalchemy.dialects import mysql
from sqlalchemy_utils.types import UUIDType


class BaseRecordModel:

    # Basic information
    id = db.Column(
        UUIDType,
        primary_key=True,
        default=uuid.uuid4,
    )

    # Timestamp (SQLAlchemy-Utils timestamp model does not have support for fractional seconds).
    created = db.Column(
        db.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
        default=datetime.utcnow,
        nullable=False,
    )

    # Timestamp (SQLAlchemy-Utils timestamp model does not have support for fractional seconds).
    updated = db.Column(
        db.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
        default=datetime.utcnow,
        nullable=False,
    )

    # Flag to soft-delete records.
    is_deleted = db.Column(db.Boolean(), default=False)


__all__ = "BaseRecordModel"
