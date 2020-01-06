from typing import Set

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
            # TODO (rob): justify the use of -0.25 here
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

    def pk_rating(self, idx: int, depth: int = 2, decay: float = 1.0):
        """
        PK-rating of a node
        :param idx: the node of which to find the PK-rating
        :param depth: the number of levels of influence to use, default 2
        :param decay: the exponential fall-off of value of ratings by level of relation, default 1.0 (none)
        :return: the PK-rating of the node
        """
        # TODO (rob): decay causes small PK-ratings, scale up by roughly decay^(1-depth),
        #             either at end or at each recursive step?
        if depth < 2:  # PK-rating simplifies to P-rating
            return self.p_rating(idx)
        nds = self.__g.neighbors(idx)
        if len(nds) == 0:
            return 0
        pk_ratings = [self.__pk_rating(n, {idx}, depth - 1, decay) for n in nds]
        # doesn't need to handle None returns from __pk_rating as calling with depth > 0
        return sum(pk_ratings) / len(nds)

    def __pk_rating(self, idx: int, used: Set[int], depth: int = 0, decay: float = 1.0):
        """
        Recursive method to find intermediate PK-rating values
        :param idx: the node being considered
        :param used: the nodes already used (the path of recursion)
        :param depth: the number of levels of recursion to go
        :param decay: the exponential fall-off of value of ratings by level of relation
        :return: the intermediate PK-rating value
        """
        if depth == 0:
            return self.get_rating(idx)
        nds = self.__g.neighbors(idx)
        if len(nds) == 0:
            return self.get_rating(idx) or 0
        # `used` set is to make sure we don't go back on ourselves when we recurse
        pk_ratings = [self.__pk_rating(n, used | {idx}, depth-1, decay) for n in nds if n not in used]
        pk_ratings = [decay * r for r in pk_ratings if r is not None]  # filter out None values and decay
        rating = self.get_rating(idx)
        if rating is not None:
            # decay is applied to layer below, but not to the actual rating of this node
            return (sum(pk_ratings) + rating) / (len(pk_ratings) + 1)
        return sum(pk_ratings) / len(pk_ratings)

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

    # returns list of influential nodes, k is cost of info
    def is_influential(self, c, k=0.2):
        g_ = self.copy()
        prev_p = g_.eval_graph()
        if g_.get_rating(c) and g_.get_rating(c) < 1 - k:
            g_.bribe(c, k)  # bribe for information
            reward = g_.eval_graph() - prev_p - k
            if reward > 0:
                return True
        return False

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
