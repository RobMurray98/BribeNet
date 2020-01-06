from bribery.briber import Briber
from graphGenerator import RatingGraph


# On each move will bribe the most influential node
class OneMoveINB(Briber):
    def __init__(self, g, u0, k=0.01):
        super().__init__(g, u0)
        # Make sure that k is set such that there are enough resources left to
        # actually bribe people.
        k = min(0.5 * (u0 / g.customer_count()), k)
        self.k = k
        self.influencers = []

    # sets influencers to ordered list of most influential nodes
    # returns amount spent
    def get_influencers(self):
        self.influencers = []
        cost_of_influence = 0
        for c in self.g.get_customers():
            prev_p = self.g.eval_graph()
            # if voted and less that cost of info
            if self.g.get_rating(c) and self.g.get_rating(c) < 1 - self.k:
                self.bribe(c, self.k)  # bribe for information
                cost_of_influence += self.k
                reward = self.g.eval_graph() - prev_p - self.k
                if reward > 0:
                    self.influencers.append((reward, c))
        # Sort based on highest reward
        self.influencers = sorted(self.influencers, key=lambda x: -x[0])
        return cost_of_influence

    # returns node bribed number
    def next_bribe(self):
        cost_of_influence = self.get_influencers()
        if self.influencers:
            (r, c) = self.influencers[0]
            cost = self.max_rating - self.g.get_rating(c)
            self.bribe(c, cost)
            self.spent.append(cost_of_influence + cost)
            return c
        else:
            self.spent.append(cost_of_influence)
            return 0


def main():
    rg = RatingGraph()
    inb = OneMoveINB(rg, 10)
    inb.get_influencers()
    inb.next_bribe()


if __name__ == '__main__':
    main()
