# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_permissions import BasePermissionPolicy
from invenio_records_permissions.generators import AuthenticatedUser, SystemProcess


class BaseRecordPermissionPolicy(BasePermissionPolicy):
    """Access control configuration for deposit operations."""

    #
    # High level permissions
    #
    can_use = [AuthenticatedUser(), SystemProcess()]

    can_manage = [AuthenticatedUser(), SystemProcess()]

    #
    # Low level permissions
    #
    can_create = [AuthenticatedUser(), SystemProcess()]

    can_read = can_use

    can_update = can_manage

    can_delete = can_manage

    can_search = can_use
