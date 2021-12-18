# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import pkg_resources


def load_plugins_entrypoint(entry_point_group: str, load_callable: bool = False):
    """Initialize plugins entry point."""

    plugins_definition = []
    for entry_point in pkg_resources.iter_entry_points(group=entry_point_group):

        entry_point_obj = entry_point.load()
        if load_callable and callable(entry_point_obj):
            entry_point_obj = entry_point_obj()

        plugins_definition.append(entry_point_obj)
    return plugins_definition
