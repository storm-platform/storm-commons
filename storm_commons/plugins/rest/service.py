# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_commons.services.service import BaseInvenioService


class PluginService(BaseInvenioService):
    """Service with plugins support."""

    @property
    def plugin_manager(self):
        """Plugin manager instance."""
        return self._plugin_manager

    def __init__(self, plugin_manager, config):
        super(PluginService, self).__init__(config)

        self._plugin_manager = plugin_manager

    def list_plugin_services(self):
        """List the available service plugin metadata."""
        return self.plugin_manager.services()
