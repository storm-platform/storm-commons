# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from marshmallow import validate


def marshmallow_not_blank_field(**kwargs):
    """Returns a non-blank validation rule.
    See:
        This code was adapted from: https://github.com/inveniosoftware/invenio-communities/blob/837f33f1c0013a69fcec0ef188200a99fafddc47/invenio_communities/communities/schema.py#L21
    """
    max_ = kwargs.get("max", "")
    return validate.Length(
        error=f"Not empty string and less than {max_} characters allowed.",
        min=1,
        **kwargs,
    )
