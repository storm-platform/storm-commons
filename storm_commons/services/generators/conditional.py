# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from abc import ABC, abstractmethod

from pydash import py_
from itertools import chain

from invenio_records_permissions.generators import Generator


class BaseConditionalGenerator(ABC, Generator):
    """Base generator to enable the creation of conditional generators."""

    @abstractmethod
    def generators(self, record):
        """Choose between 'then' or 'else' generators."""

    def needs(self, record=None, **kwargs):
        """Needs to granting permission."""

        # in the chain above is checked if the
        # ``g`` has ``needs``. In this case is assumed
        # that ``g`` is a ``Generator``. Otherwise, is
        # assumed that ``g`` is a ``flask_principal.Need``.
        return list(
            set(
                chain.from_iterable(
                    [
                        g.needs(record=record, **kwargs) if hasattr(g, "needs") else [g]
                        for g in self.generators(record)
                    ]
                )
            )
        )


class IfFinished(BaseConditionalGenerator):
    """IfFinished generator.

    This conditional generator check if a record is finished (based on an arbitrary field):

        IfFinished(
            field = 'data.is_finished',
            then_ = [<Generator>, <Generator>,],
            else_ = [<Generator>, <Generator>,]
        )

    Note:
        The ideia and base implementation of the conditional generators is presented in the
        Invenio-RDM-Records, so, thanks invenio team for this.
    """

    def __init__(self, field, then_, else_):
        self.field = field
        self.then_ = then_
        self.else_ = else_

    def generators(self, record):
        """Choose between 'then' or 'else' generators."""
        if record is None:
            return self.else_

        # getting the field using pydash
        # (handle properties and keys equally)
        value = py_.get(record, self.field)
        if value:
            return self.then_
        return self.else_


class AllGenerator(BaseConditionalGenerator):
    """AllGenerator generator.

    This conditional generator check if all arbitrary fields are truth to define the needs:

        AndGenerator(
            fields = ['data.is_finished', 'data.parent.is_finished'],
            then_ = [<Generator>, <Generator>,],
            else_ = [<Generator>, <Generator>]
        )

    In the example below, if all fields defined in the ``fields`` argument are truth (has associated value)
    so the ``then_`` generators are used, otherwise ``else_`` are used.
    """

    def __init__(self, fields, then_, else_):
        self.fields = fields
        self.then_ = then_
        self.else_ = else_

    def generators(self, record):
        """Choose between 'then' or 'else' generators."""
        if record is None:
            return self.else_

        # getting the field using pydash
        # (handle properties and keys equally)
        all_fields_are_valid = all(py_.get(record, field) for field in self.fields)

        if all_fields_are_valid:
            return self.then_
        return self.else_
