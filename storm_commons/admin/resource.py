# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import g

from flask_resources import response_handler, resource_requestctx
from invenio_records_resources.resources.records.resource import RecordResource

from storm_commons.resources.parsers import request_view_args


class AdminRecordResource(RecordResource):
    """Resource with features for record access administration."""

    @request_view_args
    @response_handler()
    def admin_add_agent(self):
        """Add a new agent."""
        edited_record = self.service.admin_add_agent(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.view_args["user_type"],
            resource_requestctx.view_args["user_id"],
        )
        return edited_record.to_dict(), 200

    @request_view_args
    @response_handler()
    def admin_remove_agent(self):
        """Remove an existing agent from a record."""
        edited_record = self.service.admin_remove_agent(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            resource_requestctx.view_args["user_type"],
            resource_requestctx.view_args["user_id"],
        )
        return edited_record.to_dict(), 200

    @request_view_args
    @response_handler()
    def admin_list_agents(self):
        """Remove an existing agent from a record."""
        agents_available = self.service.admin_list_agents(
            g.identity, resource_requestctx.view_args["pid_value"]
        )
        return agents_available, 200
