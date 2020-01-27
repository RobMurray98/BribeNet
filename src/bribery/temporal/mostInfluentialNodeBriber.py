from bribery.static.mostInfluentialNodeBriber import MostInfluentialNodeBriber as StaticMostInfluentialNodeBriber
from bribery.temporal.briber import TemporalBriber
from bribery.temporal.briberyAction import BriberyAction


class MostInfluentialNodeBriber(TemporalBriber, StaticMostInfluentialNodeBriber):

    def next_action(self) -> BriberyAction:
        pass

    # TODO: implement different behaviour that returns BriberyAction
