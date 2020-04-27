import random

from bribery.static.briber import StaticBriber

DELTA = 0.001  # ensures total bribes do not exceed budget


class RandomBriber(StaticBriber):

    def _next_bribe(self):
        customers = self.get_graph().get_customers()
        # array of random bribes
        bribes = [random.uniform(0.0, 1.0) for _ in customers]
        bribes = [b * (self.get_resources() - DELTA) / sum(bribes) for b in bribes]
        # enact bribes
        for i in customers:
            self.bribe(i, bribes[i])
