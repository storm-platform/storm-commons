# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_db import db
from invenio_records.errors import MissingModelError

from storm_commons.records.model import BaseRecordModel


class BaseRecordModelAPI:
    """Base class to access and manipulate SQLAlchemy models."""

    model_cls = BaseRecordModel
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

            db.session.add(obj.model)

        if commit:
            db.session.commit()
        return obj

    @classmethod
    def get_record(cls, with_deleted=False, **kwargs):
        """Get record by arbitrary attribute(s)."""
        with db.session.no_autoflush:
            query = cls.model_cls.query.filter_by(**kwargs)
            if not with_deleted:
                query = query.filter(cls.model_cls.is_deleted != True)

            obj = query.one()
            return cls(model=obj)

    @classmethod
    def get_records(cls, with_deleted=False, **kwargs):
        """Get record by arbitrary attribute(s)."""
        with db.session.no_autoflush:
            query = cls.model_cls.query.filter_by(**kwargs)
            if not with_deleted:
                query = query.filter(cls.model_cls.is_deleted != True)

            objs = query.all()
            return [cls(model=obj) for obj in objs]

    def commit(self, **kwargs):
        """Commit the record model changes in the database."""
        if self.model is None:
            raise MissingModelError()

        with db.session.begin_nested():
            db.session.merge(self.model)

        return self


__all__ = "BaseRecordModelAPI"
