# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.pagination import Pagination
from invenio_records_resources.services.errors import QuerystringValidationError
from invenio_records_resources.services.records.params import ParamInterpreter

from invenio_records_resources.resources import RecordResourceConfig


class BasePaginationParam(ParamInterpreter):
    """Base pagination evaluator.

    This param interpreter validates the search params (`size`, `page`). Please, note that,
    since this interpreter does not use the `search` object, its returns None.
    """

    def apply(self, identity, search, params):
        """Evaluate the query str on the search."""
        options = self.config.pagination_options

        default_size = options["default_results_per_page"]

        params.setdefault("size", default_size)
        params.setdefault("page", 1)

        p = Pagination(
            params["size"],
            params["page"],
            options["default_max_results"],
        )

        if not p.valid():
            raise QuerystringValidationError("Invalid pagination parameters.")

        return None
