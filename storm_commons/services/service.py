# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_db import db

from invenio_records_resources.services.base import Service
from invenio_records_resources.services import ServiceSchemaWrapper


class SimpleServiceBase(Service):
    """Service base class for building API without indexing and other invenio stuffs.

    Note:
        This class should be used in experimental and tiny APIs. To handle with big data files
        and many records, please use the invenio-records and invenio-*-resources classes.
    """

    @property
    def record_cls(self):
        """Service record API class."""
        return self.config.record_cls

    @property
    def schema(self):
        """Service record schema."""
        return ServiceSchemaWrapper(self, schema=self.config.schema)

    def create(self, identity, data):
        """Create record object in the datastore.

        Args:
            identity (flask_principal.Identity): Identity of user creating the record.

            data (dict): Input data according to the selected service schema.

        Returns:
            `config.record_cls`: Object API of the created record.
        """
        return self._create(self.record_cls, identity, data)

    def _create(self, record_cls, identity, data):
        """Create record object in the datastore.

        Returns:
            `config.record_cls`: Object API of the created record.
        """
        self.require_permission(identity, "create")

        # Validate input data
        data, errors = self.schema.load(
            data, context={"identity": identity}, raise_errors=True
        )

        # It's the components who saves the actual data in the record.
        record = record_cls.create()

        # Run components
        for component in self.components:
            if hasattr(component, "create"):
                component.create(identity, record=record, data=data)

        # Saving the data
        db.session.commit()

        return record

    def read(self, identity, id_):
        """Read a record from the datastore.

        Args:
            identity (flask_principal.Identity): Identity of user creating the record.

            id_ (Union[uuid.uuid4, str, int]): Record Id to read from the datastore.

        Returns:
            `config.record_cls`: Object API of the created record.
        """
        # Resolve and require permission
        record = self.record_cls.get_record(id=id_)
        self.require_permission(identity, "read", record=record)

        # Run components
        for component in self.components:
            if hasattr(component, "read"):
                component.read(identity, record=record)

        return record


class PluginService(SimpleServiceBase):
    """Service with plugins support."""

    @property
    def plugin_manager(self):
        """Plugin manager instance."""
        return self._plugin_manager

    def __init__(self, plugin_manager, config):
        super(PluginService, self).__init__(config)

        self._plugin_manager = plugin_manager

    def list_plugin_services(self):
        """List the available service plugin metadata."""
        return self.plugin_manager.services()


__all__ = ("SimpleServiceBase", "PluginService")
