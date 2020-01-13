import random
from copy import deepcopy
from typing import Optional

import numpy as np

from bribery.briber import Briber
from bribery.nonBriber import NonBriber
from graph.ratingGraph import RatingGraph, DEFAULT_GEN


class SingleBriberRatingGraph(RatingGraph):

    def __init__(self, briber: Optional[Briber], generator=DEFAULT_GEN, **kwargs):
        self.__tmp_briber = briber
        self.__tmp_kwargs = kwargs
        super().__init__(generator, specifics=self.specifics, **kwargs)

    def specifics(self):
        self._bribers: Briber = self.__tmp_briber or NonBriber(0)
        # noinspection PyTypeChecker
        self._votes = np.repeat(None, len(self._g.nodes()))
        # Generate random ratings network
        if "random_init_lower_bound" in self.__tmp_kwargs.keys():
            lower_bound = self.__tmp_kwargs["random_init_lower_bound"]
        else:
            lower_bound = -0.25
        for n in self._g.nodes():
            rating = random.uniform(lower_bound, self._max_rating)
            if rating >= 0:
                self._votes[n] = rating
        del self.__tmp_briber, self.__tmp_kwargs

    def graph(self):
        return self._g

    def _neighbours(self, node_id, *args):
        return [n for n in self._g.neighbors(node_id) if self.get_vote(n)]

    # mean of neighbouring nodes for id
    def _p_rating(self, node_id, *args):
        ns = self._neighbours(node_id)
        if len(ns) == 0:
            return 0
        return sum(self.get_vote(n) for n in ns) / len(ns)

    def _median_p_rating(self, node_id, *args):
        ns = self._neighbours(node_id)
        ns = sorted(ns, key=lambda x: self.get_vote(x))
        return self.get_vote(ns[len(ns) // 2])

    def _sample_p_rating(self, node_id, *args):
        ns = self._neighbours(node_id)
        sub = random.sample(ns, random.randint(1, len(ns)))
        return sum(self.get_vote(n) for n in sub) / len(sub)

    def _o_rating(self):
        ns = [n for n in self._g.nodes() if self.get_vote(n)]
        return sum(self.get_vote(n) for n in ns) / len(ns)

    def is_influential(self, node_id, k=0.2, rating_method=None, *args):
        g_ = deepcopy(self)
        prev_p = g_.eval_graph()
        if g_.get_vote(node_id) and g_.get_vote(node_id) < 1 - k:
            g_.bribe(node_id, k)  # bribe for information
            reward = g_.eval_graph(rating_method) - prev_p - k
            if reward > 0:
                return True
        return False

    def bribe(self, node_id, b, *args):
        if self.get_vote(node_id):
            self._votes[node_id] = min(self._max_rating, self.get_vote(node_id) + b)
        else:
            self._votes[node_id] = min(self._max_rating, b)

    # evaluates reward of graph by summing ratings
    def eval_graph(self, rating_method=None, *args):
        return sum(self.get_rating(n, rating_method=rating_method) for n in self._g.nodes())
