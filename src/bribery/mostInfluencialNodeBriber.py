from bribery.briber import Briber


# An extension to influential that bribes only the most important people
# by considering each of their effectiveness and bribing them in order
# of effectiveness (rather than bribing anyone that does better than 0)
class MostInfluentialNodeBriber(Briber):
    def __init__(self, g, u0, k=0.2):
        super().__init__(g, u0)
        # Make sure that k is set such that there are enough resources left to
        # actually bribe people.
        k = min(0.5 * (u0 / g.customer_count()), k)
        self.k = k

    def next_bribe(self):
        influencers = []
        for c in self.g.get_customers():
            prev_p = self.g.eval_graph()
            # if voted and less that cost of info
            if self.g.get_rating(c) and self.g.get_rating(c) < 1 - self.k:
                self.bribe(c, self.k)  # bribe for information
                reward = self.g.eval_graph() - prev_p - self.k
                if reward > 0:
                    influencers.append((reward, c))

        # Sort based on highest reward
        influencers = sorted(influencers, key=lambda x: -x[0])
        for (_, c) in influencers:
            self.bribe(c, self.max_rating - self.g.get_rating(c))
