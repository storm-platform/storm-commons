# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import request

from invenio_records_resources.services.records.components import ServiceComponent


class RecordAccessDefinitionComponent(ServiceComponent):
    """Access component to versioned records without parent.

    In the current implementation of this Component, it is assumed that
    the records have a systemfield ``access`` of type
    ``storm_commons.records.systemfields.fields.access.RecordAccessField``.
    """

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

    def update(
        self,
        identity,
        data=None,
        record=None,
        agent_type=None,
        agent_id=None,
        operation=None,
        **kwargs
    ):
        """update access handler."""
        if all([record, agent_type, agent_id, operation]):

            # store where the agent will
            # be added/removed.
            type_mapper = {
                "contributor": "contributors",
                "owner": "owners",
            }
            type_key = type_mapper.get(agent_type)

            if type_key:

                agent_store = getattr(record.access, type_key)
                if operation == "add":
                    # getting the type of user and assign it
                    # to access object.
                    agent_store.append({"user": agent_id})

                elif operation == "remove":
                    # finding the index: here we use
                    # the ``agent_id`` as a basis to avoid
                    # ``agent`` classes definition.
                    agent_obj = list(
                        filter(lambda x: x.agent_id == agent_id, agent_store)
                    )

                    if agent_obj:
                        agent_obj = agent_obj[0]
                        agent_store.remove(agent_obj)


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
