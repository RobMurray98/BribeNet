from bribery.temporal.briber import TemporalBriber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction


class OneMoveInfluentialNodeBriber(TemporalBriber):

    def next_action(self) -> SingleBriberyAction:
        pass

    # TODO: implement influential node behaviour that returns BriberyAction
