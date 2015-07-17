import weakref

from rpgsim.person import Person
from utils.class_utils import Borg


class Tavern(Borg):
    def __init__(self):
        super(Tavern, self).__init__()
        self._guests = weakref.WeakSet([])

    def __contains__(self, person):
        if not isinstance(person, Person):
            error_msg = 'Expecting argument of type {}, got {}'
            raise TypeError(error_msg.format(Person.__name__,
                                             person.__class__.__name__))

        return person in self._guests

    def admit(self, person):
        """Puts a person or persons into tavern."""
        if not isinstance(person, Person) and not hasattr(person, '__iter__'):
            error_msg = 'Expecting argument of type {} or iterable, got {}'
            raise TypeError(error_msg.format(Person.__name__,
                                             person.__class__.__name__))

        if hasattr(person, '__iter__'):
            for p in person:
                self.admit(p)
        else:
            if person not in self._guests:
                self._guests.add(person)

    def boot(self, person):
        """Kick a person or persons out of the tavern."""
        if not isinstance(person, Person) and not hasattr(person, '__iter__'):
            error_msg = 'Expecting argument of type {} or iterable, got {}'
            raise TypeError(error_msg.format(Person.__name__,
                                             person.__class__.__name__))

        if hasattr(person, '__iter__'):
            for p in person:
                self.boot(p)
        else:
            try:
                self._guests.remove(person)
            except KeyError:
                raise Exception('{} is not in {}'.format(person, Tavern.__name__))

    @property
    def guests(self):
        return set(self._guests)
