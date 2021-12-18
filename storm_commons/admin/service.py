# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.services.records import RecordService
from invenio_records_resources.services.uow import unit_of_work, RecordCommitOp


class AdminRecordService(RecordService):
    """Service with features for record access administration.

    Note:
        To use this service the following items are required:
            - Identity with permissions to perform ``manage_access`` actions;
            - Component with ``update`` method available to change the record permission;
            - Record with a ``access``systemfield of type ``storm_commons.records.systemfields.fields.access.RecordAccessField``.

        In the future, the need for the specific type of systemfield must be removed.
    """

    def __init__(self, config):
        super(AdminRecordService, self).__init__(config)

    def _edit_record_access(
        self, identity, record_id, user_type, user_id, operation, uow
    ):
        """Edit project access."""
        # loading the record
        record = self.record_cls.pid.resolve(record_id)

        # checking permissions
        self.require_permission(identity, "manage_access", record=record)

        self.run_components(
            "update",
            identity,
            data=record,
            record=record,
            agent_id=user_id,
            agent_type=user_type,
            operation=operation,
            uow=uow,
        )

        uow.register(RecordCommitOp(record, self.indexer))
        return self.result_item(self, identity, record, links_tpl=self.links_item_tpl)

    @unit_of_work()
    def admin_add_agent(self, identity, record_id, user_type, user_id, uow=None):
        """Add a new agent to an existing record.

        Args:
            identity (flask_principal.Identity): User identity

            record_id (str): Record id

            user_type (str): Type of user that will be added.

            user_id (str): User id

        Returns:
            Dict: The updated record document.
        """
        return self._edit_record_access(
            identity, record_id, user_type, user_id, "add", uow
        )

    @unit_of_work()
    def admin_remove_agent(self, identity, record_id, user_type, user_id, uow=None):
        """Remove an existing agent from an existing record.

        Args:
            identity (flask_principal.Identity): User identity

            record_id (str): Record id

            user_type (str): Type of user that will be added.

            user_id (str): User id

        Returns:
            Dict: The updated record document.
        """
        return self._edit_record_access(
            identity, record_id, user_type, user_id, "remove", uow
        )

    def admin_list_agents(self, identity, record_id):
        """Get record access field."""
        # loading the record
        record = self.record_cls.pid.resolve(record_id)

        # checking permissions
        self.require_permission(identity, "manage_access", record=record)

        self.run_components(
            "list",
            identity,
            record=record,
        )

        # experimental: this is a experimental
        # service function. So, in the future, probably
        # this will be changed.
        return record.get("access")
