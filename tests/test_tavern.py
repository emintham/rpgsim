from unittest import TestCase

from rpgsim.person import Person
from rpgsim.tavern import Tavern


class TavernTests(TestCase):
    def setUp(self):
        self.tavern = Tavern()
        self.person = Person()

    def test_admit(self):
        other = Person()

        self.tavern.admit(self.person)

        self.assertTrue(self.person in self.tavern)
        self.assertTrue(other not in self.tavern)

    def test_boot(self):
        self.tavern.admit(self.person)
        self.assertTrue(self.person in self.tavern)

        self.tavern.boot(self.person)
        self.assertTrue(self.person not in self.tavern)

    def test_boot_non_guest_raises_error(self):
        with self.assertRaises(Exception):
            self.tavern.boot(self.person)

    def test_tavern_is_borg(self):
        t2 = Tavern()
        self.tavern.admit(self.person)
        self.assertTrue(self.person in t2)
