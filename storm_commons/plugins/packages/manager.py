# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


class PluginManager:
    def __init__(self, plugin_services: dict):

        self._plugin_services = plugin_services

    def exists(self, service_name: str):
        """Check if a plugin service exists."""
        return service_name in self._plugin_services

    def service(self, service_name: str):
        """Get existing service."""
        if self.exists(service_name):
            return self._plugin_services.get(service_name)
        raise NotImplemented("Service not implemented yet.")

    def services(self):
        """List all available services."""
        return [
            dict(id=plugin.id, metadata=plugin.metadata)
            for plugin in self._plugin_services.values()
        ]


__all__ = "PluginManager"
