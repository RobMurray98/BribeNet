import random
from bribery.briber import Briber


# randomly picks node and gives max bribe to node
# operates one node at a time
class OneMoveRandom(Briber):

    def next_bribe(self):
        customers = self.g.get_customers()
        # pick random customer from list
        c = random.choice(customers)
        if not self.g.get_rating(c):
            self.bribe(c, self.max_rating)
        else:
            self.bribe(c, self.max_rating - self.g.get_rating(c))
        return c
