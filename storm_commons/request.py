# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from werkzeug.local import LocalProxy
from flask import request, has_request_context


def _current_access_token():
    """Current user access token."""

    if has_request_context():
        return request.args.get(
            "access_token",
        )
    return None


current_access_token = LocalProxy(_current_access_token)

__all__ = "current_access_token"
