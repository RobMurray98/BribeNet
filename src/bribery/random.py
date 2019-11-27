import random
from bribery.briber import Briber


# randomly assigns utility to bribes
class RandomBriber(Briber):

    def next_bribe(self):
        customers = self.g.get_customers()
        # array of random bribes
        bribes = [random.uniform(0.0, 1.0) for _ in customers]
        bribes = [b * self.u / sum(bribes) for b in bribes]
        # enact bribes
        for i in customers:
            self.bribe(i, bribes[i])
