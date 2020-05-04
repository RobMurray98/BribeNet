import random

import numpy as np

from BribeNet.bribery.static.briber import StaticBriber


class OneMoveRandomBriber(StaticBriber):

    def _next_bribe(self):
        customers = self.get_graph().get_customers()
        # pick random customer from list
        c = random.choice(customers)
        max_rating = self.get_graph().get_max_rating()
        vote = self.get_graph().get_vote(c)[self.get_briber_id()]
        if np.isnan(vote):
            self.bribe(c, max_rating)
        else:
            self.bribe(c, max_rating - vote)
        return c
