# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_commons.services.pagination.params import BasePaginationParam


class BaseSearchOptions:
    """Base definition for the search operations."""

    #
    # Pagination options
    #
    pagination_options = {"default_results_per_page": 25, "default_max_results": 10000}

    #
    # Parameters interpreters
    #
    params_interpreters_cls = [BasePaginationParam]
