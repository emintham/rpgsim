from unittest import TestCase

from pykka.registry import ActorRegistry

from rpgsim.entity import Entity
from rpgsim.tavern import Tavern


class TavernTests(TestCase):
    def setUp(self):
        self.tavern = Tavern()
        self.entity = Entity()

    def tearDown(self):
        ActorRegistry.stop_all()

    def test_admit(self):
        other = Entity()

        self.tavern.admit(self.entity)

        self.assertTrue(self.entity in self.tavern)
        self.assertTrue(other not in self.tavern)

    def test_admit_multiple(self):
        entities = [Entity() for _ in range(5)]
        self.tavern.admit(entities)
        self.assertEqual(self.tavern.guests, set(entities))

    def test_boot(self):
        self.tavern.admit(self.entity)
        self.assertTrue(self.entity in self.tavern)

        self.tavern.boot(self.entity)
        self.assertTrue(self.entity not in self.tavern)

    def test_boot_multiple(self):
        entities = [Entity() for _ in range(5)]
        self.tavern.admit(entities)

        self.tavern.boot(entities[:3])

        self.assertEqual(self.tavern.guests, set(entities[3:]))

    def test_boot_non_guest_raises_error(self):
        with self.assertRaises(Exception):
            self.tavern.boot(self.entity)

    def test_tavern_is_borg(self):
        t2 = Tavern()
        self.tavern.admit(self.entity)
        self.assertTrue(self.entity in t2)

    def test_tavern_guests(self):
        entities = [Entity() for _ in range(5)]
        self.tavern.admit(entities)
        self.assertEqual(self.tavern.guests, set(entities))
