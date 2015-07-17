from unittest import TestCase

from rpgsim.stats import Stats
from rpgsim.entity import Entity
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


class EntityTests(TestCase):
    def test_default_name(self):
        entity = Entity()
        self.assertEqual(entity.name, DEFAULT_NAME)

    def test_entity_can_be_named(self):
        entity = Entity(name='Joe')
        self.assertEqual(entity.name, 'Joe')

    def test_can_set_default_stats(self):
        entity = Entity(default=True)
        default_stats = Stats()
        self.assertEqual(entity.stats, default_stats)

    def test_entity_has_randomized_stats(self):
        entity = Entity()
        default_stats = Stats()
        bools = [default_stats[stat] == entity.stats[stat]
                 for stat, _ in DEFAULT_STATS.iteritems()]
        self.assertFalse(all(bools))

    def test_init_entity_with_stats(self):
        stats = Stats(strength=1, hp=200)
        entity = Entity(stats=stats)

        self.assertEqual(entity.stats['strength'], 1)
        self.assertEqual(entity.stats['hp'], 200)
