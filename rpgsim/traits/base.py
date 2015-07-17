from abc import abstractmethod
from brownie.abstract import AbstractClassMeta


class Trait(object):
    """
    Abstract Trait class that all traits inherit from.
    """

    __metaclass__ = AbstractClassMeta

    def __getattr__(self, attr):
        """
        Hijack getattr so that any predicate method beginning with
        'is_' can be safely used on Traits even if the Trait class
        or any of its superclasses do not define such a predicate.
        Returns False on such predicates.
        """
        if attr.startswith('__'):
            raise AttributeError(attr)

        try:
            return super(Trait, self).__getattr__(attr)
        except AttributeError:
            if attr.startswith('is_'):
                return False
            else:
                raise


class Observable(Trait):
    """This entity is observable."""

    is_observable = True


class Mortal(Trait):
    """This entity can be damaged."""

    __metaclass__ = AbstractClassMeta

    is_mortal = True

    @abstractmethod
    def defend(self, message):
        """Nobody wants to die"""
        return
