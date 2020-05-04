import random

from BribeNet.bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from BribeNet.bribery.temporal.briber import TemporalBriber

DELTA = 0.001  # ensures total bribes do not exceed budget


class RandomBriber(TemporalBriber):

    def _next_action(self) -> SingleBriberyAction:
        customers = self.get_graph().get_customers()
        # array of random bribes
        bribes = [random.uniform(0.0, 1.0) for _ in customers]
        bribes = [b * (max(0.0, self.get_resources() - DELTA)) / sum(bribes) for b in bribes]
        bribery_dict = {i: bribes[i] for i in customers}
        return SingleBriberyAction(self, bribes=bribery_dict)
