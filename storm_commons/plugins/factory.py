# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from .services import load_service_plugins


def plugin_factory(app, entrypoint_group_name):
    """Flask factory app to initialize the flask extensions plugins."""

    available_services = {}
    available_plugins = load_service_plugins(entrypoint_group_name, load_callable=False)

    for available_plugin_cls in available_plugins:
        # factoring the plugin flask extension
        plugin_obj = available_plugin_cls(app)

        available_services.update(plugin_obj.plugin_services)
    return available_services
