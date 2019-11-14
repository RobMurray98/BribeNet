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
        initP = self.g.evalGraph()
        customers = self.g.getCustomers()
        # array of random bribes
        brbs = [random.uniform(0.0, 1.0) for i in customers]
        brbs = [b * self.u / sum(brbs) for b in brbs]
        #enact bribes
        for i in customers:
            self.bribe(i, brbs[i])
        #reassign utility based on new ratings
        newP = self.g.evalGraph()
        self.u += newP - initP

# Can see P-rating, can't see graph
class influentialNodeBriber(briber):
    def nextBribe(self):
        k = 0.2
        for c in self.g.getCustomers():
            prevP = self.g.evalGraph()
            #if voted and less that cost of info
            if self.g.getRating(c) and self.g.getRating(c) < 1 - k:
                self.bribe(c, k) # bribe for information
                reward = self.g.evalGraph() - prevP - k
                if reward > 0:
                    #max out customers rating
                    self.bribe(c, self.maxRating - self.g.getRating(c))

            self.u += self.g.evalGraph() - prevP

def main():
    g = ratingGraph()
    inb = influentialNodeBriber(g, 100.0)
    print(inb.u)
    for i in range(20):
        inb.nextBribe()
        print(inb.u)



if __name__ == '__main__':
    main()
