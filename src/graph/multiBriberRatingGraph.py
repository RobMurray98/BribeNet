import random
from copy import deepcopy
from typing import Tuple

import numpy as np

from bribery.briber import Briber
from graph.ratingGraph import RatingGraph, DEFAULT_GEN


# provides view of rating graph for briber
class MultiBriberRatingGraph(RatingGraph):

    def __init__(self, bribers: Tuple[Briber], generator=DEFAULT_GEN, **kwargs):
        assert len(bribers) > 1  # should be at least two bribers, otherwise use SingleBriberRatingGraph
        self.__tmp_bribers = bribers
        self.__tmp_kwargs = kwargs
        super().__init__(generator, specifics=self.specifics, **kwargs)

    def specifics(self):
        self._bribers: Tuple[Briber] = self.__tmp_bribers
        # noinspection PyTypeChecker
        self._votes = np.zeros(len(self._g.nodes()), len(self._bribers))
        # Generate random ratings network
        if "random_init_lower_bound" in self.__tmp_kwargs.keys():
            lower_bound = self.__tmp_kwargs["random_init_lower_bound"]
        else:
            lower_bound = -0.25
        for n in self._g.nodes():
            for b in enumerate(self._bribers):
                rating = random.uniform(lower_bound, self._max_rating)
                if rating >= 0:
                    self._votes[n][b] = rating
        del self.__tmp_bribers, self.__tmp_kwargs

    def graph(self):
        return self._g

    def _neighbours(self, node_id, briber_id):
        return [n for n in self._g.neighbors(node_id) if self.get_vote(n)[briber_id]]

    # mean of neighbouring nodes for id
    def _p_rating(self, node_id, briber_id):
        ns = self._neighbours(node_id, briber_id)
        if len(ns) == 0:
            return 0
        return sum(self.get_vote(n) for n in ns) / len(ns)

    def _median_p_rating(self, node_id, briber_id):
        ns = self._neighbours(node_id, briber_id)
        ns = sorted(ns, key=lambda x: self.get_vote(x))
        return self.get_vote(ns[len(ns) // 2])

    def _sample_p_rating(self, node_id, briber_id):
        ns = self._neighbours(node_id, briber_id)
        sub = random.sample(ns, random.randint(1, len(ns)))
        return sum(self.get_vote(n) for n in sub) / len(sub)

    # mean of rating for all nodes
    def _o_rating(self):
        ns = [n for n in self._g.nodes() if self.get_vote(n)]
        return sum(self.get_vote(n) for n in ns) / len(ns)

    # returns customer ids without knowledge of edges or ratings
    def get_customers(self):
        return list(self._g.nodes())

    # returns list of influential nodes, k is cost of info
    def is_influential(self, node_id, k, briber_id, rating_method=None):
        g_ = deepcopy(self)
        prev_p = g_.eval_graph(briber_id)
        if g_.get_vote(node_id) and g_.get_vote(node_id) < 1 - k:
            g_.bribe(node_id, k, briber_id)  # bribe for information
            reward = g_.eval_graph(briber_id) - prev_p - k
            if reward > 0:
                return True
        return False

    def customer_count(self):
        return len(self._g.nodes())

    # increase rating by bribe (up to max 5.0)
    def bribe(self, node_id, b, briber_id):
        if self.get_vote(node_id):
            self._votes[node_id] = min(self._max_rating, self.get_vote(node_id) + b)
        else:
            self._votes[node_id][briber_id] = min(self._max_rating, b)

    # evaluates reward of graph by summing P-ratings
    def eval_graph(self, briber_id, rating_method=None):
        return sum(self.get_rating(n, briber_id, rating_method=rating_method) for n in self._g.nodes())