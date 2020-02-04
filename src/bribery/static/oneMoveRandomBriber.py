import random
import numpy as np

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
        vote = self._g.get_vote(c)[self.get_briber_id()]
        if np.isnan(vote):
            self.bribe(c, max_rating)
        else:
            self.bribe(c, max_rating - vote)
        return c
