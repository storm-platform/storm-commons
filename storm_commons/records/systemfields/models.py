# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from invenio_records.models import RecordMetadata
from invenio_accounts.models import User as InvenioUser


class Agent:
    """Generic agent abstraction to abstract User and Projects.

    Note:
        This class is based on the amazing ``invenio-rdm-records``. Is specific, I
        use as a reference the ``ParentRecordAccess`` class and the related features.

    See:
        Reference class: https://github.com/inveniosoftware/invenio-rdm-records/blob/f3877c2b1482e3c951dc0a261f6cb8ea14a1cb16/invenio_rdm_records/records/systemfields/access/owners.py#L14
    """

    #
    # Supported types
    #
    agent_cls = {"user": InvenioUser, "project": RecordMetadata}

    #
    # Loaders
    #
    agent_cls_loaders = {
        "user": lambda x: InvenioUser.query.get(x),
        "project": lambda x: RecordMetadata.query.get(x),
    }

    def __init__(self, agent):
        """Create an agent object from a `dict` or `invenio_accounts.models.User`."""

        self._entity = None
        self.agent_id = None
        self.agent_type = None

        if isinstance(agent, dict):
            keys = set(agent.keys())

            if keys.intersection(self.agent_cls.keys()):
                _key = keys.pop()  # hey! only one key is expected

                self.agent_type = _key
                self.agent_id = agent[_key]

                # finding the entity object
                agent_cls = self.agent_cls.get(_key)
                self._entity = (
                    self.agent_cls_loaders.get(_key)(self.agent_id)
                    if agent_cls
                    else None
                )
            else:
                raise ValueError("Unknown owner type: {}".format(agent))
        else:
            for agent_type in self.agent_cls:

                _entity = self.agent_cls.get(agent_type)

                if isinstance(agent, _entity):
                    self._entity = _entity

                    self.agent_id = agent.id
                    self.agent_type = agent_type

        if not all([self.agent_id, self.agent_type]):
            raise TypeError("Invalid agent type: {}".format(type(agent)))

    def dump(self):
        """Dump the owner to a dictionary."""
        return {self.agent_type: self.agent_id}

    def resolve(self):
        """Resolve the owner entity (e.g. User) via a database query."""
        return self._entity

    def __hash__(self):
        """Return hash(self)."""
        return hash(self.agent_type) + hash(self.agent_id)

    def __eq__(self, other):
        """Return self == other."""
        if type(self) != type(other):
            return False

        return self.agent_type == other.agent_type and self.agent_id == other.agent_id

    def __ne__(self, other):
        """Return self != other."""
        return not self == other

    def __str__(self):
        """Return str(self)."""
        return str(self.resolve())

    def __repr__(self):
        """Return repr(self)."""
        return repr(self.resolve())


class AgentList(list):
    """A list of agents for a record."""

    agent_cls = Agent

    def __init__(self, agents=None, agent_cls=None):
        """Create a new list of agents."""
        self.agent_cls = agent_cls or self.agent_cls

        for agent in agents or []:
            self.add(agent)

    def add(self, agent):
        """Alias for self.append(agent)."""
        self.append(agent)

    def append(self, agent):
        """Add the agent to a list of agents."""
        if not isinstance(agent, self.agent_cls):
            agent = self.agent_cls(agent)

        if agent not in self:
            super().append(agent)

    def extend(self, agents):
        """Add all new items from the specified agent to this list."""
        for agent in agents:
            self.add(agent)

    def remove(self, agent):
        """Remove the specified owner from the list of owners.

        Args:
            agent (Agents.agent_cls): Agent object to remove from the list.
        """
        if not isinstance(agent, self.agent_cls):
            owner = self.agent_cls(agent)

        super().remove(agent)

    def dump(self):
        """Dump the agents as a list of agent dictionaries."""
        return [agent.dump() for agent in self]
