from bribery.temporal.briber import TemporalBriber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction


class NonBriber(TemporalBriber):

    def next_action(self) -> SingleBriberyAction:
        return SingleBriberyAction(self)
