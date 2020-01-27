from random import random

from bribery.briber import BriberyGraphNotSetException
from bribery.temporal.briber import TemporalBriber
from bribery.temporal.briberyAction import BriberyAction


class RandomBriber(TemporalBriber):

    def next_action(self) -> BriberyAction:
        if self._g is None:
            raise BriberyGraphNotSetException()
        customers = self._g.get_customers()
        # array of random bribes
        bribes = [random.uniform(0.0, 1.0) for _ in customers]
        bribes = [b * self._u / sum(bribes) for b in bribes]
        bribery_dict = {i: bribes[i] for i in customers}
        return BriberyAction(bribery_dict)
