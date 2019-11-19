from bribery.briber import Briber


# Can see P-rating, can't see graph
class InfluentialNodeBriber(Briber):
    def __init__(self, g, u0, k=0.2):
        super().__init__(g, u0)
        # Make sure that k is set such that there are enough resources left to
        # actually bribe people.
        k = min(0.5 * (u0 / g.customerCount()), k)
        self.k = k

    def next_bribe(self):
        for c in self.g.getCustomers():
            prev_p = self.g.evalGraph()
            # if voted and less that cost of info
            if self.g.getRating(c) and self.g.getRating(c) < 1 - self.k:
                self.bribe(c, self.k)  # bribe for information
                reward = self.g.evalGraph() - prev_p - self.k
                if reward > 0:
                    # max out customers rating
                    self.bribe(c, self.maxRating - self.g.getRating(c))
