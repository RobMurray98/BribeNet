import networkit as nk
import random
import numpy as np
from types import SimpleNamespace

ws_gen = nk.generators.WattsStrogatzGenerator(30, 5, 0.3)

# provides view of rating graph for briber
class ratingGraph:

    def __init__(self, generator=ws_gen):
        # Generate random ratings network
        self.__g = generator.generate()
        self.ratings = np.repeat(None, len(self.__g.nodes()))
        self.maxRating = 1
        for n in self.__g.nodes():
            rating = random.uniform(-0.25, self.maxRating)
            if(rating >= 0):
                self.ratings[n] = rating

    def graph(self):
        return self.__g

    #mean of neighbouring nodes for id
    def pRating(self, id):
        nds = [n for n in self.__g.neighbors(id) if self.getRating(n)]
        if len(nds) == 0:
            return 0
        return sum(self.getRating(n) for n in nds) / len(nds)

    def medianPRating(self, id):
        ns = [n for n in self.__g.neighbors(id) if self.getRating(n)]
        ns = sorted(ns, key = lambda x: self.getRating(x))
        return self.getRating(ns[len(ns) // 2])

    def samplePRating(self, id):
        ns = [n for n in self.__g.neighbors(id) if self.getRating(n)]
        sub = random.sample(ns, random.randint(1, len(ns)))
        return sum(self.getRating(n) for n in sub) / len(sub)

    #mean of rating for all nodes
    def oRating(self):
        nds = [n for n in self.__g.nodes() if self.getRating(n)]
        return sum(self.getRating(n) for n in nds) / len(nds)

    #returns customer ids without knowledge of edges or ratings
    def getCustomers(self):
        return list(self.__g.nodes())
    
    def customerCount(self):
        return len(self.__g.nodes())

    def getRating(self, id):
        return self.ratings[id]

    # increase rating by bribe (up to max 5.0)
    def bribe(self, id, b):
        if self.getRating(id):
            self.ratings[id] = min(self.maxRating, self.getRating(id) + b)
        else:
            self.ratings[id] = min(self.maxRating, b)

    # evaluates reward of graph by summing P-ratings
    def evalGraph(self):
        return sum(self.pRating(n) for n in self.__g.nodes())
    
    def copy(self):
        newGraph = copyGraph(self.graph())
        generator = SimpleNamespace()
        generator.generate = lambda: newGraph
        newRG = ratingGraph(generator)
        newRG.ratings = self.ratings.copy()
        newRG.maxRating = self.maxRating
        return newRG

def copyGraph(g):
    newGraph = nk.graph.Graph()
    newGraph.append(g)
    return newGraph