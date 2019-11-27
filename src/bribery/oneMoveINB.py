from bribery.briber import Briber
from graphGenerator import RatingGraph

# On each move will bribe the most influential node
class OneMoveINB(Briber):
    def __init__(self, g, u0, k=0.2):
        super().__init__(g, u0)
        # Make sure that k is set such that there are enough resources left to
        # actually bribe people.
        k = min(0.5 * (u0 / g.customer_count()), k)
        self.k = k
        self.influencers = []

    # sets influencers to ordered list of most influential nodes
    def get_influencers(self):
        self.influencers = []
        for c in self.g.get_customers():
            prev_p = self.g.eval_graph()
            # if voted and less that cost of info
            if self.g.get_rating(c) and self.g.get_rating(c) < 1 - self.k:
                self.bribe(c, self.k)  # bribe for information
                reward = self.g.eval_graph() - prev_p - self.k
                if reward > 0:
                    self.influencers.append((reward, c))
        # Sort based on highest reward
        self.influencers = sorted(self.influencers, key=lambda x: -x[0])

    #returns node bribed number
    def next_bribe(self):
        self.get_influencers()
        (r, c) = self.influencers[0]
        self.bribe(c, self.max_rating - self.g.get_rating(c))
        return c

def main():
    rg = RatingGraph()
    inb = OneMoveINB(rg, 10)
    inb.get_influencers()
    inb.next_bribe()

if __name__ == '__main__':
    main()
