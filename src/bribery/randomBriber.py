import random
from bribery.briber import Briber, BriberyGraphNotSetException


# randomly assigns utility to bribes
class RandomBriber(Briber):

    def next_bribe(self):
        if self._g is None:
            raise BriberyGraphNotSetException()
        customers = self._g.get_customers()
        # array of random bribes
        bribes = [random.uniform(0.0, 1.0) for _ in customers]
        bribes = [b * self._u / sum(bribes) for b in bribes]
        # enact bribes
        for i in customers:
            self.bribe(i, bribes[i])
