from copy import deepcopy
from random import random
from typing import Optional, List

from bribery.temporal.briber import TemporalBriber
from bribery.temporal.nonBriber import TemporalNonBriber
from graph.ratingGraph import RatingMethod, DEFAULT_GEN
from graph.temporal.ratingGraph import TemporalRatingGraph

import numpy as np


class SingleBriberTemporalRatingGraph(TemporalRatingGraph):

    def __init__(self, briber: Optional[TemporalBriber], generator=DEFAULT_GEN, specifics=None, **kwargs):
        if briber is not None:
            assert issubclass(briber.__class__, TemporalBriber), "briber must be an instance of a subclass of " \
                                                                 "TemporalBriber, or None"
        self.__tmp_briber = briber
        self.__tmp_kwargs = kwargs
        super().__init__(generator, specifics=self.__specifics, **kwargs)

    def __specifics(self):
        self._bribers: TemporalBriber = self.__tmp_briber or TemporalNonBriber(0)
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

    def step(self):
        raise NotImplementedError

    def _neighbours(self, node_id: int, *args) -> List[int]:
        return [n for n in self._g.neighbors(node_id) if self.get_vote(n)]

    def _p_rating(self, node_id: int, *args) -> float:
        ns = self._neighbours(node_id)
        if len(ns) == 0:
            return 0
        return sum(self.get_vote(n) for n in ns) / len(ns)

    def _median_p_rating(self, node_id: int, *args) -> float:
        ns = self._neighbours(node_id)
        ns = sorted(ns, key=lambda x: self.get_vote(x))
        return self.get_vote(ns[len(ns) // 2])

    def _sample_p_rating(self, node_id: int, *args) -> float:
        ns = self._neighbours(node_id)
        sub = random.sample(ns, random.randint(1, len(ns)))
        return sum(self.get_vote(n) for n in sub) / len(sub)

    def _o_rating(self, *args) -> float:
        ns = [n for n in self._g.nodes() if self.get_vote(n)]
        return sum(self.get_vote(n) for n in ns) / len(ns)

    def is_influential(self, node_id: int, k: float = 0.2, rating_method=None, *args) -> bool:
        g_ = deepcopy(self)
        prev_p = g_.eval_graph()
        if g_.get_vote(node_id) and g_.get_vote(node_id) < 1 - k:
            g_.bribe(node_id, k)  # bribe for information
            reward = g_.eval_graph(rating_method) - prev_p - k
            if reward > 0:
                return True
        return False

    def eval_graph(self, rating_method: Optional[RatingMethod] = None, *args) -> float:
        return sum(self.get_rating(n, rating_method=rating_method) for n in self._g.nodes())

    def bribe(self, node_id: int, b: float, briber_id: int):
        if self.get_vote(node_id):
            self._votes[node_id] = min(self._max_rating, self.get_vote(node_id) + b)
        else:
            self._votes[node_id] = min(self._max_rating, b)
