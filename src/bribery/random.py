import random

from bribery.briber import Briber


# randomly assigns utility to bribes
class RandomBriber(Briber):

    def next_bribe(self):
        customers = self.g.getCustomers()
        # array of random bribes
        brbs = [random.uniform(0.0, 1.0) for _ in customers]
        brbs = [b * self.u / sum(brbs) for b in brbs]
        # enact bribes
        for i in customers:
            self.bribe(i, brbs[i])
