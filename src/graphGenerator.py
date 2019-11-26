import networkit as nk
import random
import numpy as np
from types import SimpleNamespace

ws_gen = nk.generators.WattsStrogatzGenerator(30, 5, 0.3)


# provides view of rating graph for briber
class RatingGraph:

    def __init__(self, generator=ws_gen):
        # Generate random ratings network
        self.__g = generator.generate()
        # noinspection PyTypeChecker
        self.ratings = np.repeat(None, len(self.__g.nodes()))
        self.max_rating = 1
        for n in self.__g.nodes():
            rating = random.uniform(-0.25, self.max_rating)
            if rating >= 0:
                self.ratings[n] = rating

    def graph(self):
        return self.__g

    def neighbors(self, idx):
        return [n for n in self.__g.neighbors(idx) if self.get_rating(n)]

    # mean of neighbouring nodes for id
    def p_rating(self, idx):
        ns = self.neighbors(idx)
        if len(ns) == 0:
            return 0
        return sum(self.get_rating(n) for n in ns) / len(ns)

    def median_p_rating(self, idx):
        ns = self.neighbors(idx)
        ns = sorted(ns, key=lambda x: self.get_rating(x))
        return self.get_rating(ns[len(ns) // 2])

    def sample_p_rating(self, idx):
        ns = self.neighbors(idx)
        sub = random.sample(ns, random.randint(1, len(ns)))
        return sum(self.get_rating(n) for n in sub) / len(sub)

    # mean of rating for all nodes
    def o_rating(self):
        ns = [n for n in self.__g.nodes() if self.get_rating(n)]
        return sum(self.get_rating(n) for n in ns) / len(ns)

    # returns customer ids without knowledge of edges or ratings
    def get_customers(self):
        return list(self.__g.nodes())

    def customer_count(self):
        return len(self.__g.nodes())

    def get_rating(self, idx):
        return self.ratings[idx]

    # increase rating by bribe (up to max 5.0)
    def bribe(self, idx, b):
        if self.get_rating(idx):
            self.ratings[idx] = min(self.max_rating, self.get_rating(idx) + b)
        else:
            self.ratings[idx] = min(self.max_rating, b)

    # evaluates reward of graph by summing P-ratings
    def eval_graph(self):
        return sum(self.p_rating(n) for n in self.__g.nodes())

    def copy(self):
        new_graph = self.__copy_graph()
        generator = SimpleNamespace()
        generator.generate = lambda: new_graph
        new_rg = RatingGraph(generator)
        new_rg.ratings = self.ratings.copy()
        new_rg.max_rating = self.max_rating
        return new_rg

    def __copy_graph(self):
        new_graph = nk.graph.Graph()
        new_graph.append(self.graph())
        return new_graph
