import random

from config import DEFAULT_STATS, MAX_STAT


class Stats(object):
    def __init__(self, **kwargs):
        self._stats = {}
        self.max_stat = MAX_STAT

        for stat, value in DEFAULT_STATS.iteritems():
            value = kwargs.get(stat, value)
            self._stats[stat] = value

        randomize_max = kwargs.get('randomize_max', None)
        if randomize_max:
            self.randomize(randomize_max)

        self._initial = self._stats.copy()

    def __getitem__(self, stat):
        return self._stats[stat]

    def __iter__(self):
        return iter(self._stats)

    def __eq__(self, other):
        if not isinstance(other, Stats):
            error_msg = 'Cannot compare {} to {}'
            raise TypeError(error_msg.format(Stats.__name__,
                                             other.__class__.__name__))
        return self._stats == other._stats

    def fmt_stat(self, stat):
        value = self._stats[stat]
        return stat + ': ' + str(value)

    def __repr__(self):
        stat_strs = [self.fmt_stat(stat) for stat in DEFAULT_STATS.iterkeys()]
        output = ', '.join(stat_strs)

        return '<{}: '.format(self.__class__.__name__) + output + '>'

    @property
    def initial_stats(self):
        return self._initial

    def randomize(self, n=MAX_STAT):
        self.max_stat = n

        for stat, value in DEFAULT_STATS.iteritems():
            value = random.randint(value, n)
            self._stats[stat] = value
