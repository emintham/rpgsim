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
        """Puts a person into tavern."""
        if not isinstance(person, Person):
            error_msg = 'Expecting argument of type {}, got {}'
            raise TypeError(error_msg.format(Person.__name__,
                                             person.__class__.__name__))

        if person not in self._guests:
            self._guests.add(person)

    def boot(self, person):
        """Kick a person out of the tavern."""
        if not isinstance(person, Person):
            error_msg = 'Expecting argument of type {}, got {}'
            raise TypeError(error_msg.format(Person.__name__,
                                             person.__class__.__name__))

        try:
            self._guests.remove(person)
        except KeyError:
            raise Exception('{} is not in {}'.format(person, Tavern.__name__))

    @property
    def guests(self):
        return list(self._guests)
