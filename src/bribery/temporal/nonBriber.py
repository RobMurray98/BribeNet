from bribery.temporal.briber import TemporalBriber
from bribery.temporal.briberyAction import BriberyAction


class TemporalNonBriber(TemporalBriber):

    def next_action(self) -> BriberyAction:
        pass

    # TODO: implement behaviour that returns an empty BriberyAction
