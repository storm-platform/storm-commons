# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import request

from invenio_records_resources.services.records.components import ServiceComponent


class RecordAccessDefinitionComponent(ServiceComponent):
    """Access component to versioned records without parent."""

    def create(self, identity, data=None, record=None, **kwargs):
        """Add basic ownership fields to the record."""
        if record:
            # getting the project context
            project_id = request.view_args.get("project_id")

            # creating the objects
            _prj_obj = {"project": project_id}
            _user_obj = {"user": identity.id}

            # in the code below, we assume that the owners
            # is always a project and the users go in the
            # contributors section.
            record.access.owners.append(_prj_obj)
            record.access.contributors.append(_user_obj)


class VersionedRecordAccessDefinitionComponent(ServiceComponent):
    """Access component to versioned records with parent."""

    def _create(self, identity, data=None, record=None, **kwargs):
        """Extra ``create`` method operation."""
        pass

    def create(self, identity, data=None, record=None, **kwargs):
        """Add basic ownership fields to the record."""

        parent = record.parent
        if parent:
            parent.access.contributors.append({"user": identity.id})

            # extra method: this method was added to users provides
            # arbitrary functions for the ``create`` operation.
            self._create(identity, data, record, **kwargs)
