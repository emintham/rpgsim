from unittest import TestCase

from rpgsim.traits import Observable, Mortal


class NoDefend(Mortal):
    """
    This mortal does not know how to defend. Evolution would
    have weeded out this trait, thankfully the almighty Python
    would prevent instantiation of this object.
    """


class Immortal(Observable):
    """
    The immortal does not die and does not know how to defend
    but we can still ask whether it is mortal.
    """


class UnobservableMortal(Mortal):
    """
    This mortal is so good at hiding one really should question
    whether it exists...
    """

    thinks = True

    @property
    def exists(self):
        return self.thinks

    def defend(self, message):
        pass


class TraitTests(TestCase):
    def test_mortals_must_implement_defend(self):
        with self.assertRaises(TypeError):
            NoDefend()

    def test_any_predicate_works_on_all_traits(self):
        immortal = Immortal()
        self.assertFalse('is_mortal' in dir(immortal))
        self.assertFalse(immortal.is_mortal)

        unobservable = UnobservableMortal()
        self.assertFalse('is_observable' in dir(unobservable))
        self.assertFalse(unobservable.is_observable)
        self.assertTrue(unobservable.exists)
