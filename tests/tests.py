from unittest import TestCase

from rpgsim.stats import Stats
from rpgsim.person import Person
from config import DEFAULT_STATS, MAX_STAT, DEFAULT_NAME


class StatsTests(TestCase):
    def test_stat_initialization(self):
        stats = Stats()
        for stat, value in DEFAULT_STATS.iteritems():
            actual = stats[stat]
            self.assertEqual(actual, value)

    def test_stat_randomized_initialization(self):
        stats = Stats(randomize_max=50)
        for stat, default in DEFAULT_STATS.iteritems():
            actual = stats[stat]
            self.assertTrue(actual <= 50)
            self.assertTrue(default <= actual)

    def test_stat_randomize(self):
        stats = Stats()
        stats.randomize()
        for stat, default in DEFAULT_STATS.iteritems():
            actual = stats[stat]
            self.assertTrue(actual <= MAX_STAT)
            self.assertTrue(default <= actual)


class PersonTests(TestCase):
    def test_default_name(self):
        person = Person()
        self.assertEqual(person.name, DEFAULT_NAME)

    def test_person_can_be_named(self):
        person = Person(name='Joe')
        self.assertEqual(person.name, 'Joe')

    def test_can_set_default_stats(self):
        person = Person(default=True)
        default_stats = Stats()
        self.assertEqual(person.stats, default_stats)

    def test_person_has_randomized_stats(self):
        person = Person()
        default_stats = Stats()
        bools = [default_stats[stat] == person.stats[stat]
                 for stat, _ in DEFAULT_STATS.iteritems()]
        self.assertFalse(all(bools))

    def test_init_person_with_stats(self):
        stats = Stats(strength=1, hp=200)
        person = Person(stats=stats)

        self.assertEqual(person.stats['strength'], 1)
        self.assertEqual(person.stats['hp'], 200)
