# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask_resources import (
    JSONDeserializer,
    JSONSerializer,
    RequestBodyParser,
    ResourceConfig,
    ResponseHandler,
)

from storm_commons.resources.args import BaseSearchRequestArgsSchema


class BaseResourceConfig(ResourceConfig):
    """Base configuration class for job resources."""

    # Request parsing
    request_read_args = {}
    request_view_args = {}  # defined in the concrete implementations.
    request_search_args = BaseSearchRequestArgsSchema
    request_body_parsers = {"application/json": RequestBodyParser(JSONDeserializer())}
    default_content_type = "application/json"

    # Response handling
    response_handlers = {"application/json": ResponseHandler(JSONSerializer())}
    default_accept_mimetype = "application/json"


__all__ = "BaseResourceConfig"
