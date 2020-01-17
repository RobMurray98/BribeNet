from copy import deepcopy
from random import random
from typing import Optional, List, Tuple

from bribery.temporal.briber import TemporalBriber
from graph.ratingGraph import RatingMethod, DEFAULT_GEN
from graph.temporal.ratingGraph import TemporalRatingGraph

import numpy as np


class MultiBriberTemporalRatingGraph(TemporalRatingGraph):

    def __init__(self, bribers: Tuple[TemporalBriber], generator=DEFAULT_GEN, **kwargs):
        assert isinstance(bribers, tuple), "bribers must be a tuple of instances of subclasses of StaticRatingBriber"
        assert len(bribers) > 1, "should be at least two bribers, otherwise use SingleBriberRatingGraph"
        for b in bribers:
            assert issubclass(b.__class__, TemporalBriber), "member of bribers tuple not an instance of a subclass " \
                                                            "of TemporalBriber"
        self.__tmp_bribers = bribers
        self.__tmp_kwargs = kwargs
        super().__init__(generator, specifics=self.__specifics, **kwargs)

    def __specifics(self):
        self._bribers: Tuple[TemporalBriber] = self.__tmp_bribers
        # noinspection PyTypeChecker
        self._votes = np.zeros((len(self._g.nodes()), len(self._bribers)))
        # Generate random ratings network
        if "random_init_lower_bound" in self.__tmp_kwargs.keys():
            lower_bound = self.__tmp_kwargs["random_init_lower_bound"]
        else:
            lower_bound = -0.25
        for n in self._g.nodes():
            for b, _ in enumerate(self._bribers):
                rating = random.uniform(lower_bound, self._max_rating)
                if rating >= 0:
                    self._votes[n][b] = rating
        del self.__tmp_bribers, self.__tmp_kwargs

    def step(self):
        raise NotImplementedError

    def _neighbours(self, node_id: int, briber_id: int) -> List[int]:
        return [n for n in self._g.neighbors(node_id) if self.get_vote(n)[briber_id]]

    def _p_rating(self, node_id: int, briber_id: int) -> float:
        ns = self._neighbours(node_id, briber_id)
        if len(ns) == 0:
            return 0
        return sum(self.get_vote(n)[briber_id] for n in ns) / len(ns)

    def _median_p_rating(self, node_id: int, briber_id: int) -> float:
        ns = self._neighbours(node_id, briber_id)
        ns = sorted(ns, key=lambda x: self.get_vote(x)[briber_id])
        return self.get_vote(ns[len(ns) // 2])[briber_id]

    def _sample_p_rating(self, node_id: int, briber_id: int) -> float:
        ns = self._neighbours(node_id, briber_id)
        sub = random.sample(ns, random.randint(1, len(ns)))
        return sum(self.get_vote(n)[briber_id] for n in sub) / len(sub)

    def _o_rating(self, briber_id: int) -> float:
        ns = [n for n in self._g.nodes() if self.get_vote(n)[briber_id]]
        return sum(self.get_vote(n)[briber_id] for n in ns) / len(ns)

    def is_influential(self, node_id: int, k: float, briber_id: int, rating_method=None) -> bool:
        g_ = deepcopy(self)
        prev_p = g_.eval_graph(briber_id, rating_method)
        if g_.get_vote(node_id)[briber_id] is not None and (g_.get_vote(node_id)[briber_id] < 1 - k):
            g_.bribe(node_id, k, briber_id)  # bribe for information
            reward = g_.eval_graph(briber_id, rating_method) - prev_p - k
            if reward > 0:
                return True
        return False

    def eval_graph(self, briber_id: int, rating_method: Optional[RatingMethod] = None) -> float:
        return sum(self.get_rating(node_id=n, briber_id=briber_id, rating_method=rating_method)
                   for n in self._g.nodes())

    def bribe(self, node_id: int, b: float, briber_id: int):
        if self._votes[node_id][briber_id]:
            self._votes[node_id][briber_id] = min(self._max_rating, self._votes[node_id][briber_id] + b)
        else:
            self._votes[node_id][briber_id] = min(self._max_rating, b)
