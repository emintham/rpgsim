import weakref

from rpgsim.entity import Entity
from utils.class_utils import Borg


class Tavern(Borg):
    def __init__(self):
        super(Tavern, self).__init__()
        self._guests = weakref.WeakSet([])

    def __contains__(self, entity):
        if not isinstance(entity, Entity):
            error_msg = 'Expecting argument of type {}, got {}'
            raise TypeError(error_msg.format(Entity.__name__,
                                             entity.__class__.__name__))

        return entity in self._guests

    def __len__(self):
        return len(self.guests)

    def __repr__(self):
        prefix = '<{}({}): '.format(self.__class__.__name__, str(len(self)))
        suffix = '>'
        return prefix + self.fmt_guests() + suffix

    def fmt_guests(self):
        return ', '.join([str(guest) for guest in self.guests])

    def admit(self, entity):
        """Puts a entity or entities into tavern."""
        if not isinstance(entity, Entity) and not hasattr(entity, '__iter__'):
            error_msg = 'Expecting argument of type {} or iterable, got {}'
            raise TypeError(error_msg.format(Entity.__name__,
                                             entity.__class__.__name__))

        if hasattr(entity, '__iter__'):
            for p in entity:
                self.admit(p)
        else:
            if entity not in self._guests:
                self._guests.add(entity)

    def boot(self, entity):
        """Kick a entity or entities out of the tavern."""
        if not isinstance(entity, Entity) and not hasattr(entity, '__iter__'):
            error_msg = 'Expecting argument of type {} or iterable, got {}'
            raise TypeError(error_msg.format(Entity.__name__,
                                             entity.__class__.__name__))

        if hasattr(entity, '__iter__'):
            for p in entity:
                self.boot(p)
        else:
            try:
                self._guests.remove(entity)
            except KeyError:
                raise Exception('{} is not in {}'.format(entity, Tavern.__name__))

    @property
    def guests(self):
        return set(self._guests)
