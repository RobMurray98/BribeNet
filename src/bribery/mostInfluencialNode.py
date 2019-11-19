from bribery.briber import Briber


# An extension to influential that bribes only the most important people
# by considering each of their effectiveness and bribing them in order
# of effectiveness (rather than bribing anyone that does better than 0)
class MostInfluentialNodeBriber(Briber):
    def __init__(self, g, u0, k=0.2):
        super().__init__(g, u0)
        # Make sure that k is set such that there are enough resources left to
        # actually bribe people.
        k = min(0.5 * (u0 / g.customerCount()), k)
        self.k = k

    def next_bribe(self):
        influencers = []
        for c in self.g.getCustomers():
            prev_p = self.g.evalGraph()
            # if voted and less that cost of info
            if self.g.getRating(c) and self.g.getRating(c) < 1 - self.k:
                self.bribe(c, self.k)  # bribe for information
                reward = self.g.evalGraph() - prev_p - self.k
                if reward > 0:
                    influencers.append((reward, c))

        # Sort based on highest reward
        influencers = sorted(influencers, key=lambda x: -x[0])
        for (_, c) in influencers:
            self.bribe(c, self.maxRating - self.g.getRating(c))
