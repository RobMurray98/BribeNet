from graphGenerator import ratingGraph
import networkx as nx
from abc import ABC
import random

#abstract briber class
class briber(ABC):
    def __init__(self, g, u0):
        self.u = u0 # resources of briber to spend
        self.g = g # network for agent

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
            self.g.bribe(i, brbs[i])
        #reassign utility based on new ratings
        self.u = self.g.evalGraph()

class regressionBriber(briber):
    def nextBribe(self):

def main():
    g = ratingGraph()
    rb = randomBriber(g, 10.0)
    rb.nextBribe()


if __name__ == '__main__':
    main()
