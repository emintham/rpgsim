import weakref

from pykka import ThreadingActor, ActorRegistry

from rpgsim.stats import Stats
from rpgsim.traits import Observable, Mortal
from config import DEFAULT_NAME


class EntityActor(ThreadingActor):
    def __init__(self, entity_ref=None):
        super(EntityActor, self).__init__()
        self.entity_ref = None
        if entity_ref is not None:
            self.entity_ref = weakref.ref(entity_ref)

    def on_receive(self, message):
        print 'received: {}'.format(message)
        action = message.get('action')
        wait = message.get('wait')

        if self.entity_ref is None:
            print 'no entity_ref'
            return

        return self.entity_ref().handle(action, message, wait)


class Entity(Observable):
    def __init__(self, name=DEFAULT_NAME, stats=None, default=False):
        if stats is not None and not isinstance(stats, Stats):
            error_msg = 'Expecting stats to be of type {}, got {} instead.'
            raise TypeError(error_msg.format(Stats.__name__,
                                             stats.__class__.__name__))

        self.name = name
        self.actor = EntityActor().start(entity_ref=self)
        self.stats = stats or Stats()
        if not default and stats is None:
            self.stats.randomize()

    def __del__(self):
        if hasattr(self, 'actor'):
            self.actor.stop()

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{}: '.format(self.__class__.__name__) + str(self) + '>'

    @property
    def uuid(self):
        # TODO: generate own uuid
        return self.actor.actor_urn

    @property
    def attack_info(self):
        return self.stats.attack_stats

    @property
    def handlers(self):
        return {}

    def tell(self, msg):
        """Proxies the message to the actor"""
        print 'was told: {}'.format(msg)
        self.actor.tell(msg)

    def ask(self, msg):
        """Proxies the message to the actor"""
        print 'was asked: {}'.format(msg)
        return self.actor.ask(msg)

    def null_handler(self, message, wait):
        """Do nothing"""
        if wait:
            return None

    def handle(self, action, message, wait=False):
        """Try to handle the incoming action."""
        try:
            print 'using handler: {}'.format(self.handlers[action])
            self.handlers[action](message, wait)
        except KeyError:
            self.null_handler(message, wait)


class Character(Mortal, Entity):
    def attack(self, other, wait):
        if not isinstance(other, Entity):
            error_msg = 'Expecting other to be of type {}, got {} instead.'
            raise TypeError(error_msg.format(Entity.__name__,
                                             other.__class__.__name__))

        if not other.is_mortal:
            return

        msg = {
            'action': 'attack',
            'attacker': self.uuid,
            'wait': wait
        }
        msg.update(self.attack_info)

        if wait:
            return other.ask(msg)
        other.tell(msg)

    @property
    def handlers(self):
        handlers = super(Character, self).handlers
        handlers.update({
            'attack': self.defend
        })
        return handlers

    def defend(self, message, wait):
        defender_stats = sum(self.attack_info.values())
        attacker_stats = sum(message.get(stat, 0)
                             for stat in self.attack_info.keys())
        damage = attacker_stats - defender_stats
        if damage > 0:
            self.stats['hp'] -= damage

        # FIXME: This is talking directly to the entity's actor...
        #        We can probably refactor this to an Entity metaclass
        #        that registers all entities by a separate uuid
        attacker = message.get('attacker')
        ActorRegistry.get_by_urn(attacker).tell({
            'action': 'damage_report',
            'damage': damage
        })
