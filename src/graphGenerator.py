import networkx as nx
import random

# provides view of rating graph for briber
class ratingGraph:

    def __init__(self):
        # Generate random ratings network
        self.__g = nx.watts_strogatz_graph(30, 5, 0.3)
        for n in self.__g.nodes:
            self.__g.nodes[n]["rating"] = random.uniform(0.0, 5.0)

    #mean of neighbouring nodes for id
    def pRating(self, id):
        tot = 0
        for n in self.__g.neighbors(id):
            tot += self.__g.nodes[n]["rating"]
        return tot / len(self.__g[id])

    #mean of rating for all nodes
    def oRating(self):
        return sum(self.__g.nodes[n]["rating"] for n in self.__g.nodes) / len(self.__g.nodes)

    #returns customer ids without knowledge of edges or ratings
    def getCustomers(self):
        return list(self.__g.nodes)

    # increase rating by bribe (up to max 5.0)
    def bribe(self, id, b):
        self.__g.nodes[id]["rating"] = min(5.0, self.__g.nodes[id]["rating"] + b)

    # evaluates reward of graph by average P-rating
    def evalGraph(self):
        tot = 0
        for n in self.__g.nodes:
            tot += self.pRating(n)
        return tot / len(self.__g.nodes)
