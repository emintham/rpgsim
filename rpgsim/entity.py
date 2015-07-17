from pykka import ThreadingActor

from rpgsim.stats import Stats
from config import DEFAULT_NAME


class EntityActor(ThreadingActor):
    def on_receive(self, message):
        pass


class Entity(object):
    def __init__(self, name=DEFAULT_NAME, stats=None, default=False):
        if stats is not None and not isinstance(stats, Stats):
            error_msg = 'Expecting stats to be of type {}, got {} instead.'
            raise TypeError(error_msg.format(Stats.__name__,
                                             stats.__class__.__name__))

        self.name = name
        self.actor = EntityActor().start()
        self.stats = stats or Stats()
        if not default and stats is None:
            self.stats.randomize()

    def __del__(self):
        self.actor.stop()

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{}: '.format(self.__class__.__name__) + str(self) + '>'
