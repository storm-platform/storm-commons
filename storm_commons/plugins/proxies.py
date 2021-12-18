# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from werkzeug.local import LocalProxy


def _current_plugin_manager(extension_name):
    """Retrieve the plugin manager of an extension."""
    from flask import current_app

    flask_extension = current_app.extensions[extension_name]
    plugin_manager = flask_extension.plugin_manager

    return plugin_manager


def extension_plugin_manager(extension_name):
    """Retrieve the plugin manager of an extension."""
    return LocalProxy(lambda: _current_plugin_manager(extension_name))


__all__ = "extension_plugin_manager"
