import random

from bribery.briber import BriberyGraphNotSetException
from bribery.static.briber import StaticBriber

DELTA = 0.001  # ensures total bribes do not exceed budget


class RandomBriber(StaticBriber):

    def next_bribe(self):
        if self._g is None:
            raise BriberyGraphNotSetException()
        customers = self._g.get_customers()
        # array of random bribes
        bribes = [random.uniform(0.0, 1.0) for _ in customers]
        bribes = [b * (self._u - DELTA) / sum(bribes) for b in bribes]
        # enact bribes
        for i in customers:
            self.bribe(i, bribes[i])
