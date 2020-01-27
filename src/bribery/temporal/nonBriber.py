from bribery.temporal.briber import TemporalBriber
from bribery.temporal.briberyAction import BriberyAction


class NonBriber(TemporalBriber):

    def next_action(self) -> BriberyAction:
        return BriberyAction()
