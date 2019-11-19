from graphGenerator import ratingGraph
import networkx as nx
from abc import ABC
import random

#abstract briber class
class briber(ABC):
    def __init__(self, g, u0):
        self.u = u0 # resources of briber to spend
        self.g = g # network for agent
        self.maxRating = self.g.maxRating

    def bribe(self, id, amount):
        if amount <= self.u:
            self.g.bribe(id, amount)
            self.u -= amount

    def nextBribe(self):
        pass

# randomly assigns utility to bribes
class randomBriber(briber):
    def nextBribe(self):
        customers = self.g.getCustomers()
        # array of random bribes
        brbs = [random.uniform(0.0, 1.0) for i in customers]
        brbs = [b * self.u / sum(brbs) for b in brbs]
        #enact bribes
        for i in customers:
            self.bribe(i, brbs[i])

# Can see P-rating, can't see graph
class influentialNodeBriber(briber):
    def __init__(self, g, u0, k=0.2):
        super(self, g, u0)
        # Make sure that k is set such that there are enough resources left to
        # actually bribe people.
        k = min(0.5 * (u0 / len(g.nodes())), k)
        self.k = k

    def nextBribe(self):
        for c in self.g.getCustomers():
            prevP = self.g.evalGraph()
            #if voted and less that cost of info
            if self.g.getRating(c) and self.g.getRating(c) < 1 - self.k:
                self.bribe(c, self.k) # bribe for information
                reward = self.g.evalGraph() - prevP - self.k
                if reward > 0:
                    #max out customers rating
                    self.bribe(c, self.maxRating - self.g.getRating(c))

# An extension to influential that bribes only the most important people
# by considering each of their effectiveness and bribing them in order
# of effectiveness (rather than bribing anyone that does better than 0)
class mostInfluentialNodeBriber(briber):
    def __init__(self, g, u0, k=0.2):
        super(self, g, u0)
        # Make sure that k is set such that there are enough resources left to
        # actually bribe people.
        k = min(0.5 * (u0 / len(g.nodes())), k)
        self.k = k

    def nextBribe(self):
        influencers = []
        for c in self.g.getCustomers():
            prevP = self.g.evalGraph()
            #if voted and less that cost of info
            if self.g.getRating(c) and self.g.getRating(c) < 1 - self.k:
                self.bribe(c, self.k) # bribe for information
                reward = self.g.evalGraph() - prevP - self.k
                if reward > 0:
                    influencers.append((reward, c))

        # Sort based on highest reward
        influencers = sorted(influencers, lambda x: -x[0])
        for (_, c) in influencers:
            self.bribe(c, self.maxRating - self.g.getRating(c))

def main():
    g = ratingGraph()
    inb = influentialNodeBriber(g, 100.0)
    print(inb.u)
    for _ in range(20):
        inb.nextBribe()
        print(inb.u)

if __name__ == '__main__':
    main()
