from bribery.static.randomBriber import RandomBriber as StaticRandomBriber
from bribery.temporal.briber import TemporalBriber
from bribery.temporal.briberyAction import BriberyAction


class RandomBriber(TemporalBriber, StaticRandomBriber):

    def next_action(self) -> BriberyAction:
        pass

    # TODO: implement different behaviour that returns BriberyAction
