from bribery.static.oneMoveInfluentialNodeBriber import OneMoveInfluentialNodeBriber \
    as StaticOneMoveInfluentialNodeBriber
from bribery.temporal.briber import TemporalBriber
from bribery.temporal.briberyAction import BriberyAction


class OneMoveInfluentialNodeBriber(TemporalBriber, StaticOneMoveInfluentialNodeBriber):

    def next_action(self) -> BriberyAction:
        pass

    # TODO: implement different behaviour that returns BriberyAction
