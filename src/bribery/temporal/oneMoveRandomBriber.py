from bribery.static.oneMoveRandomBriber import OneMoveRandomBriber as StaticOneMoveRandomBriber
from bribery.temporal.briber import TemporalBriber
from bribery.temporal.briberyAction import BriberyAction


class OneMoveRandomBriber(TemporalBriber, StaticOneMoveRandomBriber):

    def next_action(self) -> BriberyAction:
        pass

    # TODO: implement different behaviour that returns BriberyAction
