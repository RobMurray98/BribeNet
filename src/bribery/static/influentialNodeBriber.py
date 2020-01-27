from bribery.briber import BriberyGraphNotSetException


from bribery.static.briber import StaticBriber


class InfluentialNodeBriber(StaticBriber):
    def __init__(self, u0, k=0.2):
        super().__init__(u0)
        self.k = k

    def _set_graph(self, g):
        super()._set_graph(g)
        # Make sure that k is set such that there are enough resources left to actually bribe people.
        self.k = min(0.5 * (self._u / self._g.customer_count()), self.k)

    def next_bribe(self):
        if self._g is None:
            raise BriberyGraphNotSetException()
        for c in self._g.get_customers():
            prev_p = self._g.eval_graph()
            # if voted and less that cost of info
            if self._g.get_vote(c) and self._g.get_vote(c) < 1 - self.k:
                self.bribe(c, self.k)  # bribe for information
                reward = self._g.eval_graph() - prev_p - self.k
                if reward > 0:
                    # max out customers rating
                    self.bribe(c, self._g.get_max_rating() - self._g.get_vote(c))
