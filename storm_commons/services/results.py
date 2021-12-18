# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.pagination import Pagination
from invenio_records_resources.services.base import ServiceItemResult, ServiceListResult


class BaseItemResult(ServiceItemResult):
    """Single record result."""

    @property
    def links(self):
        """Get links for the defined result item."""
        return self._links_tpl.expand(self._record)

    @property
    def data(self):
        """Property to get the record data."""
        if self._data:
            return self._data

        self._data = self._schema.dump(
            self._record, context=dict(identity=self._identity, record=self._record)
        )
        if self._links_tpl:
            self._data["links"] = self.links

        return self._data

    def __init__(self, service, identity, record, links_tpl=None, schema=None):
        self._record = record
        self._schema = schema
        self._service = service
        self._identity = identity
        self._links_tpl = links_tpl

        self._data = None

    def to_dict(self):
        """Get a dictionary for the record."""
        return self.data


class BaseListResult(ServiceListResult):
    """List of records results.

    This base class was implemented based on ``flask_sqlalchemy.Pagination``.  Thus, the result
    passed to the class must be an ``SQLAlchemy pagination object.``.
    """

    @property
    def pagination(self):
        """Record list pagination."""
        return Pagination(self._params["size"], self._params["page"], self.total)

    @property
    def items(self):
        """Result item iterator."""
        for result in self._results.items:
            # Load model
            record = self._service.record_cls(model=result)

            yield BaseItemResult(
                self._service,
                self._identity,
                record,
                self._links_item_tpl,
                self._schema,
            ).to_dict()

    @property
    def total(self):
        """Get total number of items in the result."""
        return self._results.total

    def __len__(self):
        """Number of result items."""
        return self.total

    def __init__(
        self,
        service,
        identity,
        results,
        params=None,
        links_tpl=None,
        links_item_tpl=None,
        schema=None,
    ):
        self._service = service
        self._identity = identity
        self._results = results
        self._schema = schema
        self._params = params
        self._links_tpl = links_tpl
        self._links_item_tpl = links_item_tpl

    def to_dict(self):
        res = {"hits": {"hits": list(self.items), "total": self.total}}

        if self._params:
            if self._links_tpl:
                res["links"] = self._links_tpl.expand(self.pagination)

        return res


__all__ = ("BaseItemResult", "BaseListResult")
