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


class BaseSQLAlchemyModel:

    #
    # Cache basic information
    #
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


class BaseSQLAlchemyModelAPI:
    """Base class to access and manipulate SQLAlchemy models."""

    model_cls = BaseSQLAlchemyModel
    """SQLAlchemy model class defining which table stores the records."""

    def __init__(self, model=None):
        self.model = model

    @property
    def id(self):
        """Get model identifier."""
        return self.model.id if self.model else None

    @property
    def created(self):
        """Get creation timestamp."""
        return self.model.created if self.model else None

    @property
    def updated(self):
        """Get last updated timestamp."""
        return self.model.updated if self.model else None

    @classmethod
    def create(cls, commit=False, **kwargs):
        """Create a new docker image entry."""

        with db.session.begin_nested():
            obj = cls(model=cls.model_cls(**kwargs))

            # saving
            db.session.add(obj.model)

        if commit:
            db.session.commit()
        return obj

    @classmethod
    def get_record(cls, **kwargs):
        """Get record by arbitrary attribute(s)."""
        with db.session.no_autoflush:
            query = cls.model_cls.query.filter_by(**kwargs)

            obj = query.one()
            return cls(model=obj)

    @classmethod
    def get_records(cls, **kwargs):
        """Get record by arbitrary attribute(s)."""
        with db.session.no_autoflush:
            query = cls.model_cls.query.filter_by(**kwargs)

            objs = query.all()
            return [cls(model=obj) for obj in objs]


__all__ = ("BaseSQLAlchemyModel", "BaseSQLAlchemyModelAPI")
