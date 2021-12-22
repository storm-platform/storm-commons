# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from invenio_records_resources.services.base.links import LinksTemplate


class ActionLinksTemplate(LinksTemplate):
    """Templates for generating links with action objects."""

    def __init__(self, links, links_action, context=None):
        """Initializer."""
        super(ActionLinksTemplate, self).__init__(links, context=context)

        self._links_action = links_action

    def expand(self, obj):
        """Expand all the link templates."""

        links = {"actions": {}}
        ctx = self.context
        for key, link in self._links.items():
            if link.should_render(obj, ctx):
                links[key] = link.expand(obj, ctx)

        # expanding the links actions.
        for action_name, action_link in self._links_action.items():
            if action_link.should_render(obj, ctx):
                links["actions"][action_name] = action_link.expand(obj, ctx)

        return links


__all__ = "ActionLinksTemplate"
