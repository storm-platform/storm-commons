# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_db import db

from invenio_records_resources.services.base import Service
from invenio_records_resources.services import ServiceSchemaWrapper, LinksTemplate


class BaseInvenioService(Service):
    """Base class service for building API without Elasticsearch indexing and other invenio stuffs.

    Note:
        This class should be used in experimental and tiny APIs. To handle big data files
        and many records, please use the Invenio-records and Invenio-[Record/Draft]-Resources Classes.
    """

    @property
    def record_cls(self):
        """Service record API class."""
        return self.config.record_cls

    @property
    def schema(self):
        """Service record schema."""
        return ServiceSchemaWrapper(self, schema=self.config.schema)

    @property
    def links_item_tpl(self):
        return LinksTemplate(self.config.links_item)

    def create(self, identity, data):
        """Create record object in the datastore.

        Args:
            identity (flask_principal.Identity): Identity of user creating the record.

            data (dict): Input data according to the selected service schema.

        Returns:
            `config.result_item_cls`: Created record as a ResultItem object.
        """
        self.require_permission(identity, "create")

        # Validate input data
        data, errors = self.schema.load(
            data, context={"identity": identity}, raise_errors=True
        )

        # It's the components who saves the actual data in the record.
        record = self.record_cls.create()

        # Run components
        for component in self.components:
            if hasattr(component, "create"):
                component.create(identity, record=record, data=data)

        # Saving the data
        db.session.commit()

        return self.result_item(
            self,
            identity,
            record,
            links_tpl=self.links_item_tpl,
            schema=self.schema,
        )

    def read(self, identity, id_):
        """Read a record from the datastore.

        Args:
            identity (flask_principal.Identity): Identity of user creating the record.

            id_ (Union[uuid.uuid4, str, int]): Record Id to read from the datastore.

        Returns:
            `config.result_item_cls`: Loaded record as a ResultItem object.
        """
        # Resolve and require permission
        record = self.record_cls.get_record(id=id_)
        self.require_permission(identity, "read", record=record)

        # Run components
        for component in self.components:
            if hasattr(component, "read"):
                component.read(identity, record=record)

        return self.result_item(
            self,
            identity,
            record,
            links_tpl=self.links_item_tpl,
            schema=self.schema,
        )

    def update(self, identity, id_, data):
        """Update an existing record in the datastore.

        Args:
            identity (flask_principal.Identity): Identity of user creating the record.

            id_ (Union[uuid.uuid4, str, int]): Record Id to read from the datastore.

            data (dict): Input data according to the selected service schema.

        Returns:
            `config.result_item_cls`: updated record as ResultItem object.
        """
        # Resolve and require permission
        record = self.record_cls.get_record(id=id_)
        self.require_permission(identity, "update", record=record)

        # Validate input data
        data, errors = self.schema.load(
            data, context={"identity": identity}, raise_errors=True
        )

        # Run components
        for component in self.components:
            if hasattr(component, "update"):
                component.update(identity, record=record, data=data)

        # Saving the data
        db.session.commit()

        return self.result_item(
            self,
            identity,
            record,
            links_tpl=self.links_item_tpl,
            schema=self.schema,
        )

    def delete(self, identity, id_):
        """Update an existing record in the datastore.

        Args:
            identity (flask_principal.Identity): Identity of user creating the record.

            id_ (Union[uuid.uuid4, str, int]): Record Id to read from the datastore.

        Returns:
            None: The object is marked as deleted in the datastore.
        """
        # Resolve and require permission
        record = self.record_cls.get_record(id=id_)
        self.require_permission(identity, "delete", record=record)

        # Run components
        for component in self.components:
            if hasattr(component, "delete"):
                component.delete(identity, record=record)

        # Saving the data
        db.session.commit()

    def search(self, identity, params):
        """Search an existing record in the datastore.

        Args:
            identity (flask_principal.Identity): Identity of user creating the record.

            params (dict): Search params.

        Returns:
            `config.result_list_cls`: List of records that match the query criteria.
        """
        self.require_permission(identity, "search")

        # run search args evaluator
        # special application of args evaluator: In this case, we use
        # the evaluators only to validate/parse/inspect the user arguments.
        # These values are not used to create a `search` object like the
        # Invenio services do.
        for interpreter_cls in self.config.search.params_interpreters_cls:
            interpreter_cls(self.config.search).apply(identity, None, params)

        # extracting the parameters
        # note: This search method handle data with SQLAlchemy. So, we need to "remove"
        # the results options (in this case `size` and `page`) from the params dict.
        pagination_params = {k: v for k, v in params.items() if k in ["size", "page"]}
        query_params = {k: v for k, v in params.items() if k not in pagination_params}

        with db.session.no_autoflush:
            # querying only the valid data (not deleted).
            query = self.record_cls.model_cls.query.filter_by(
                is_deleted=False, **query_params
            )

            # paginate the results.
            search_result = query.paginate(
                page=pagination_params["page"],
                per_page=pagination_params["size"],
                error_out=False,
            )

            # create a result list object.
            # we use the ``flask_sqlalchemy.Pagination``, created in the
            # ``BaseQuery.paginate`` method above.
            return self.result_list(
                self,
                identity,
                search_result,
                params,
                links_tpl=LinksTemplate(
                    self.config.links_search, context={"args": params}
                ),
                links_item_tpl=self.links_item_tpl,
                schema=self.schema,
            )


__all__ = "BaseInvenioService"
