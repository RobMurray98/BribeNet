from bribery.briber import BriberyGraphNotSetException

from bribery.static.briber import StaticBriber


class OneMoveInfluentialNodeBriber(StaticBriber):
    def __init__(self, u0, k=0.01):
        super().__init__(u0)
        self.influencers = []
        self.k = k

    def _set_graph(self, g):
        super()._set_graph(g)
        # Make sure that k is set such that there are enough resources left to actually bribe people.
        self.k = min(0.5 * (self._u / self._g.customer_count()), self.k)

    # sets influencers to ordered list of most influential nodes
    def get_influencers(self):
        if self._g is None:
            raise BriberyGraphNotSetException()
        self.influencers = []
        for c in self._g.get_customers():
            prev_p = self._g.eval_graph()
            # if voted and less that cost of info
            if self._g.get_vote(c) and self._g.get_vote(c) < 1 - self.k:
                self.bribe(c, self.k)  # bribe for information
                reward = self._g.eval_graph() - prev_p - self.k
                if reward > 0:
                    self.influencers.append((reward, c))
        # Sort based on highest reward
        self.influencers = sorted(self.influencers, key=lambda x: -x[0])

    # returns node bribed number
    def next_bribe(self):
        if self._g is None:
            raise BriberyGraphNotSetException()
        self.get_influencers()
        if self.influencers:
            (r, c) = self.influencers[0]
            self.bribe(c, self._g.get_max_rating() - self._g.get_vote(c))
            return c
        else:
            return 0
