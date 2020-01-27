import random

from bribery.briber import BriberyGraphNotSetException
from bribery.static.briber import StaticBriber


class OneMoveRandomBriber(StaticBriber):

    def next_bribe(self):
        if self._g is None:
            raise BriberyGraphNotSetException()
        customers = self._g.get_customers()
        # pick random customer from list
        c = random.choice(customers)
        max_rating = self._g.get_max_rating()
        if not self._g.get_vote(c):
            self.bribe(c, max_rating)
        else:
            self.bribe(c, max_rating - self._g.get_vote(c))
        return c
