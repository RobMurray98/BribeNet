from bribery.briber import BriberyGraphNotSetException

from bribery.static.briber import StaticBriber
from helpers.override import override


class OneMoveInfluentialNodeBriber(StaticBriber):
    def __init__(self, u0, k=0.1):
        super().__init__(u0)
        self.influencers = []
        self._k = k  # will be reassigned when graph set

    @override
    def _set_graph(self, g):
        super()._set_graph(g)
        # Make sure that k is set such that there are enough resources left to actually bribe people.
        self._k = min(self._k, 0.5 * (self._u / self._g.customer_count()))

    # sets influencers to ordered list of most influential nodes
    def _get_influencers(self):
        if self._g is None:
            raise BriberyGraphNotSetException()
        self.influencers = []
        for c in self._g.get_customers():
            reward = self._g.is_influential(c, k=self._k, briber_id=self.get_briber_id())
            if reward > 0:
                self.influencers.append((reward, c))
        # Sort based on highest reward
        self.influencers = sorted(self.influencers, reverse=True)

    # returns node bribed number
    def _next_bribe(self):
        if self._g is None:
            raise BriberyGraphNotSetException()
        self._get_influencers()
        if self.influencers:
            (r, c) = self.influencers[0]
            self.bribe(c, self._g.get_max_rating() - self._g.get_vote(c))
            return c
        else:
            return 0
