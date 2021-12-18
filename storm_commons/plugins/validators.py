# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from marshmallow import validate

from .proxies import extension_plugin_manager


def marshmallow_validate_plugin_service(extension_name, **kwargs):
    """Validate if the selected service exists in the platform instance.

    Args:
        extension_name (str): Name of the flask extension that have the Plugin Manager
        used to check the available services.

    Returns:
        marshmallow.validate.OneOf: OneOf validator with the valid services.

    Note:
        This method use the flask application context. Please, check if you are in this context
        before use the function.
    """
    plugin_manager = extension_plugin_manager(extension_name)

    return validate.OneOf(
        choices=[service.get("id") for service in plugin_manager.services()],
        **kwargs,
    )


def marshmallow_validate_custom_plugin_schema(extension_name, service_name, **kwargs):
    """Validate if a custom metadata field has the required properties
    defined by the plugin that supports the custom fields.

    Args:
        extension_name (str): Name of the flask extension that have the Plugin Manager
        used to check the available services.

        service_name (str): Name (ID) of the plugin that provides the custom marshmallow schema to
        validate the data.

    Returns:
        None: The validation is done in the function.

    Note:
        This method use the flask application context. Please, check if you are in this context
        before use the function.
    """
    if service_name:
        plugin_manager = extension_plugin_manager(extension_name)

        # selecting the service from the current
        # plugin manager.
        service = plugin_manager.service(service_name)

        # validating
        return service.schema().load
    return lambda x: True


__all__ = (
    "marshmallow_validate_plugin_service",
    "marshmallow_validate_custom_plugin_schema",
)
