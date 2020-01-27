from bribery.static.influentialNodeBriber import InfluentialNodeBriber as StaticInfluentialNodeBriber
from bribery.temporal.briber import TemporalBriber
from bribery.temporal.briberyAction import BriberyAction


class InfluentialNodeBriber(TemporalBriber, StaticInfluentialNodeBriber):

    def next_action(self) -> BriberyAction:
        pass

    # TODO: implement different behaviour that returns BriberyAction
