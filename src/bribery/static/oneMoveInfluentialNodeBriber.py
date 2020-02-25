from bribery.briber import BriberyGraphNotSetException

from bribery.static.briber import StaticBriber
from helpers.override import override


class OneMoveInfluentialNodeBriber(StaticBriber):
    def __init__(self, u0, k=0.1):
        super().__init__(u0)
        self.influencers = []
        self.k = k  # will be reassigned when graph set

    @override
    def _set_graph(self, g):
        super()._set_graph(g)
        # Make sure that k is set such that there are enough resources left to actually bribe people.
        self.k = min(self.k, 0.5 * (self._u / self._g.customer_count()))

    # returns node bribed number
    def _next_bribe(self):
        self.influencers = []
        for c1 in self._g.get_customers():
            reward = self._g.is_influential(c1, k=self.k, briber_id=self.get_briber_id())
            if reward > 0:
                self.influencers.append((reward, c1))
        # Sort based on highest reward
        self.influencers = sorted(self.influencers, reverse=True)
        if self.influencers:
            (r, c) = self.influencers[0]
            self.bribe(c, self._g.get_max_rating() - self._g.get_vote(c))
            return c
        else:
            return 0
