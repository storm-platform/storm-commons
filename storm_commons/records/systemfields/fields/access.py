# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from invenio_records.systemfields import SystemField
from storm_commons.records.systemfields.models import AgentList


class RecordAccess:
    """Access management of a record.

    Note:
        This class is based on the amazing ``invenio-rdm-records``. Is specific, I
        use as a reference the ``ParentRecordAccess`` class and the related features.

    See:
        Reference class: https://github.com/inveniosoftware/invenio-rdm-records/blob/f3877c2b1482e3c951dc0a261f6cb8ea14a1cb16/invenio_rdm_records/records/systemfields/access/field/parent.py#L18
    """

    owners_cls = AgentList
    contributors_cls = AgentList

    @property
    def owners(self):
        """An alias for the owned_by property."""
        return self.owned_by

    @property
    def contributors(self):
        """An alias for the contributed_by property."""
        return self.contributed_by

    @classmethod
    def from_dict(cls, access_dict, owners_cls=None, contributors_cls=None):
        """Create a new Access object from the specified 'access' property.

        As specified in the ``invenio-rdm-records``:

             The new ``ParentRecordAccess`` object will be populated with new instances
             from the configured classes.

            If ``access_dict`` is empty, the ``ParentRecordAccess`` object will
            be populated with new instances of ``owners_cls``, ``contributors_cls``.
        """

        errors = []
        owners_cls = owners_cls or cls.owners_cls
        contributors_cls = contributors_cls or cls.contributors_cls

        # defining defaults
        owners = owners_cls()
        contributors = contributors_cls()

        if access_dict:
            for _list, _type in [
                (owners, "owned_by"),
                (contributors, "contributed_by"),
            ]:
                for owner_dict in access_dict.get(_type, []):
                    try:
                        _list.add(_list.agent_cls(owner_dict))
                    except Exception as e:
                        errors.append(e)

        access = cls(
            owned_by=owners,
            contributed_by=contributors,
        )
        access.errors = errors
        return access

    def __init__(
        self, owned_by=None, contributed_by=None, owners_cls=None, contributors_cls=None
    ):
        """Create a new Access object for a record."""

        owners_cls = owners_cls or self.owners_cls
        contributors_cls = contributors_cls or self.contributors_cls

        self.errors = []
        self.owned_by = owned_by if owned_by else owners_cls()
        self.contributed_by = contributed_by if contributed_by else contributors_cls()

    def dump(self):
        """Dump the field values as dictionary."""
        return {
            "owned_by": self.owned_by.dump(),
            "contributed_by": self.contributed_by.dump(),
        }

    def refresh_from_dict(self, access_dict):
        """Re-initialize the Access object with the data in the access_dict."""
        new_access = self.from_dict(access_dict)
        self.errors = new_access.errors
        self.owned_by = new_access.owned_by
        self.contributed_by = new_access.contributed_by

    def __repr__(self):
        """Return repr(self)."""
        return "<{} (owners: {}, contributors: {})>".format(
            type(self).__name__, len(self.owners or []), len(self.contributors or [])
        )


class RecordAccessField(SystemField):
    """System field for managing record access.

    Note:
        This class is based on the amazing ``invenio-rdm-records``. Is specific, I
        use as a reference the ``ParentRecordAccess`` class and the related features.

    See:
        Reference class: https://github.com/inveniosoftware/invenio-rdm-records/blob/f3877c2b1482e3c951dc0a261f6cb8ea14a1cb16/invenio_rdm_records/records/systemfields/access/field/parent.py#L143
    """

    def __init__(self, key="access", access_obj_class=RecordAccess):
        """RecordAccessField initialization."""
        self._access_obj_class = access_obj_class
        super().__init__(key=key)

    def obj(self, instance):
        """Get the access object."""
        obj = self._get_cache(instance)
        if obj is None:
            data = self.get_dictkey(instance)
            if data:
                obj = self._access_obj_class.from_dict(data)
            else:
                obj = self._access_obj_class()
            self._set_cache(instance, obj)
        return obj

    def set_obj(self, record, obj):
        """Set the access object."""
        if isinstance(obj, dict):
            obj = self._access_obj_class.from_dict(obj)

        assert isinstance(obj, self._access_obj_class)

        # From ``invenio-rdm-records``:
        # We do not dump the object until the pre_commit hook
        # I.e. record.access != record['access']
        self._set_cache(record, obj)

    def pre_commit(self, record):
        """Dump the configured values before the record is committed."""
        obj = self.obj(record)
        if obj is not None:
            # only set the 'access' property if one was present in the
            # first place -- this was a problem in the unit test:
            # tests/resources/test_resources.py:test_simple_flow
            record["access"] = obj.dump()

    def __get__(self, record, owner=None):
        """Get the record's access object."""
        if record is None:
            # access by class
            return self

        # access by object
        return self.obj(record)

    def __set__(self, record, obj):
        """Set the records access object."""
        self.set_obj(record, obj)
