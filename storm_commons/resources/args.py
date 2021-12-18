# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from marshmallow import fields, validate
from flask_resources.parsers import MultiDictSchema


class BaseSearchRequestArgsSchema(MultiDictSchema):
    """Base class for search query string arguments parsers.

    This class is based on in the `SearchRequestArgsSchema`, provided
    by `Invenio-Records-Resources`. This new implementation provides
    a simple interface to use in basic APIs without invenio super-powers
    (like elasticsearch and other stuffs).
    """

    page = fields.Int(validate=validate.Range(min=1))
    size = fields.Int(validate=validate.Range(min=1))


__all__ = "BaseSearchRequestArgsSchema"
