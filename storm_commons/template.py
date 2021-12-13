# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from jinja2 import Environment, PackageLoader


def render_template(
    template_name: str, module_name: str, package_path: str, **template_objects
):
    """Render a jinja template."""
    env = Environment(loader=PackageLoader(module_name, package_path))

    # Metadata template file
    template = env.get_template(template_name)

    # Rendering the template and cleaning the output result.
    return template.render(**template_objects)


__all__ = "render_template"
