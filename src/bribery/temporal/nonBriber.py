from bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from bribery.temporal.briber import TemporalBriber


class NonBriber(TemporalBriber):

    def _next_action(self) -> SingleBriberyAction:
        return SingleBriberyAction(self)
