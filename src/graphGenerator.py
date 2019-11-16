import networkit as nk
import random
import numpy as np

ws_gen = nk.generators.WattsStrogatzGenerator(30, 5, 0.3)

# provides view of rating graph for briber
class ratingGraph:

    def __init__(self, generator=ws_gen):
        # Generate random ratings network
        self.__g = generator()
        self.ratings = np.repeat(None, len(self.__g.nodes()))
        self.maxRating = 1
        for n in self.__g.nodes():
            rating = random.uniform(-0.25, self.maxRating)
            if(rating >= 0):
                self.ratings[n] = rating

    #mean of neighbouring nodes for id
    def pRating(self, id):
        nds = [n for n in self.__g.neighbors(id) if self.getRating(n)]
        if len(nds) == 0:
            return 0
        return sum(self.getRating(n) for n in nds) / len(nds)

    #mean of rating for all nodes
    def oRating(self):
        nds = [n for n in self.__g.nodes() if self.getRating(n)]
        return sum(self.getRating(n) for n in nds) / len(nds)

    #returns customer ids without knowledge of edges or ratings
    def getCustomers(self):
        return list(self.__g.nodes())

    def getRating(self, id):
        return self.ratings[id]

    # increase rating by bribe (up to max 5.0)
    def bribe(self, id, b):
        if self.getRating(id):
            self.ratings[id] = min(self.maxRating, self.getRating(id) + b)
        else:
            self.ratings[id] = min(self.maxRating, b)

    # evaluates reward of graph by suming P-ratings
    def evalGraph(self):
        return sum(self.pRating(n) for n in self.__g.nodes())