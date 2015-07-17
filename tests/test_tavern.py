from unittest import TestCase

from pykka.registry import ActorRegistry

from rpgsim.person import Person
from rpgsim.tavern import Tavern


class TavernTests(TestCase):
    def setUp(self):
        self.tavern = Tavern()
        self.person = Person()

    def tearDown(self):
        ActorRegistry.stop_all()

    def test_admit(self):
        other = Person()

        self.tavern.admit(self.person)

        self.assertTrue(self.person in self.tavern)
        self.assertTrue(other not in self.tavern)

    def test_admit_multiple(self):
        persons = [Person() for _ in range(5)]
        self.tavern.admit(persons)
        self.assertEqual(self.tavern.guests, set(persons))

    def test_boot(self):
        self.tavern.admit(self.person)
        self.assertTrue(self.person in self.tavern)

        self.tavern.boot(self.person)
        self.assertTrue(self.person not in self.tavern)

    def test_boot_multiple(self):
        persons = [Person() for _ in range(5)]
        self.tavern.admit(persons)

        self.tavern.boot(persons[:3])

        self.assertEqual(self.tavern.guests, set(persons[3:]))

    def test_boot_non_guest_raises_error(self):
        with self.assertRaises(Exception):
            self.tavern.boot(self.person)

    def test_tavern_is_borg(self):
        t2 = Tavern()
        self.tavern.admit(self.person)
        self.assertTrue(self.person in t2)

    def test_tavern_guests(self):
        persons = [Person() for _ in range(5)]
        self.tavern.admit(persons)
        self.assertEqual(self.tavern.guests, set(persons))
