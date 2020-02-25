from bribery.briber import BriberyGraphNotSetException

from bribery.static.briber import StaticBriber
from helpers.override import override


class MostInfluentialNodeBriber(StaticBriber):
    """
    An extension to influential that bribes only the most important people
    by considering each of their effectiveness and bribing them in order
    of effectiveness (rather than bribing anyone that does better than 0)
    """

    def __init__(self, u0, k=0.1):
        super().__init__(u0)
        self.k = k  # will be reassigned when graph set

    @override
    def _set_graph(self, g):
        super()._set_graph(g)
        # Make sure that k is set such that there are enough resources left to actually bribe people.
        self.k = min(self.k, 0.5 * (self._u / self._g.customer_count()))

    def _next_bribe(self):
        influencers = []
        for c in self._g.get_customers():
            reward = self._g.is_influential(c, k=self.k, briber_id=self.get_briber_id())
            if reward > 0:
                influencers.append((reward, c))
        # Sort based on highest reward
        influencers = sorted(influencers, reverse=True)
        for (_, c) in influencers:
            self.bribe(c, self._g.get_max_rating() - self._g.get_vote(c))
