import networkx as nx
import random

# provides view of rating graph for briber
class ratingGraph:

    def __init__(self):
        # Generate random ratings network
        self.__g = nx.watts_strogatz_graph(30, 5, 0.3)
        self.maxRating = 1
        for n in self.__g.nodes:
            rating = random.uniform(-0.25, self.maxRating)
            if(rating < 0):
                self.__g.nodes[n]["rating"] = None
            else:
                self.__g.nodes[n]["rating"] = rating

    #mean of neighbouring nodes for id
    def pRating(self, id):
        nds = [n for n in self.__g.neighbors(id) if self.getRating(n)]
        if len(nds) == 0:
            return 0
        return sum(self.getRating(n) for n in nds) / len(nds)

    #mean of rating for all nodes
    def oRating(self):
        nds = [n for n in self.__g.nodes if self.getRating(n)]
        return sum(self.getRating(n) for n in nds) / len(nds)

    #returns customer ids without knowledge of edges or ratings
    def getCustomers(self):
        return list(self.__g.nodes)

    def getRating(self, id):
        return self.__g.nodes[id]["rating"]

    # increase rating by bribe (up to max 5.0)
    def bribe(self, id, b):
        if self.getRating(id):
            self.__g.nodes[id]["rating"] = min(self.maxRating, self.getRating(id) + b)
        else:
            self.__g.nodes[id]["rating"] = min(self.maxRating, b)

    # evaluates reward of graph by suming P-ratings
    def evalGraph(self):
        return sum(self.pRating(n) for n in self.__g.nodes)
