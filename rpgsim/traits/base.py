from abc import abstractmethod
from brownie.abstract import AbstractClassMeta


class Trait(object):
    """
    Abstract Trait class that all traits inherit from.
    """

    __metaclass__ = AbstractClassMeta

    @property
    def trait_name(self):
        return ''

    @property
    def traits(self):
        return []

    def __getattr__(self, attr):
        """
        Hijack getattr so that any predicate method beginning with
        'is_' can be safely used on Traits even if the Trait class
        or any of its superclasses do not define such a predicate.
        Returns False on such predicates.
        """
        if attr.startswith('__'):
            # __getattr__ is only called if __getattribute__ fails
            # if a __method__ gets to this point, it is most likely
            # not defined.
            raise AttributeError(
                '{} not defined on {}'.format(attr, self.__class__.__name__))

        try:
            return super(Trait, self).__getattr__(attr)
        except AttributeError:
            if attr.startswith('is_'):
                return False
            else:
                raise


class BaseTrait(Trait):
    __metaclass__ = AbstractClassMeta

    @property
    def trait_name(self):
        return self.__class__.__name__.lower()

    @property
    def traits(self):
        return [self.trait_name] + super(BaseTrait, self).traits


class Observable(BaseTrait):
    """This entity is observable."""

    is_observable = True


class Mortal(BaseTrait):
    """This entity can be damaged."""

    __metaclass__ = AbstractClassMeta

    is_mortal = True

    @abstractmethod
    def defend(self, message):
        """Nobody wants to die"""
        return
