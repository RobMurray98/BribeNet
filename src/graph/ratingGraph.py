import random
from abc import ABC
from copy import deepcopy
from typing import Tuple, Optional, List, Any

import networkit as nk
import numpy as np

from graph.ratingMethod import RatingMethod

from graph.conversions import to_weighted

# noinspection PyUnresolvedReferences
DEFAULT_GEN = nk.generators.WattsStrogatzGenerator(30, 5, 0.3)


class RatingGraph(ABC):
    """
    Representation of network graph which bribers interact with
    """

    def __init__(self, bribers: Tuple[Any], generator=DEFAULT_GEN, specifics=None, **kwargs):
        """
        Implementing classes should initialise self.__true_rating and self.__bribers
        :param generator: the graph generator used to instantiate the graph
        :param specifics: function in implementing class to call after the superclass initialisation,
                          but prior to _finalise_init (template design pattern)
        :param **kwargs:  additional keyword arguments to the graph, such as max_rating
        """
        # Generate random ratings network
        self._g = generator.generate()
        self._g = to_weighted(self._g)
        from bribery.briber import Briber
        self._bribers: Tuple[Briber] = bribers
        if "max_rating" in kwargs.keys():
            self._max_rating: float = kwargs["max_rating"]
        else:
            self._max_rating: float = 1.0
        self._votes: np.ndarray[Optional[float]] = None
        self._truths: np.ndarray[float] = None
        self._rating_method: RatingMethod = RatingMethod.P_RATING
        if specifics is not None:
            specifics()
        self._finalise_init()

    def _finalise_init(self):
        """
        Perform assertions that ensure everything is initialised
        """
        assert isinstance(self._bribers, tuple), "specifics of implementing class did not instantiate self._bribers " \
                                                 "as a tuple"
        from bribery.briber import Briber
        for briber in self._bribers:
            assert issubclass(briber.__class__, Briber)
            # noinspection PyProtectedMember
            briber._set_graph(self)
        assert isinstance(self._votes, np.ndarray), "specifics of implementing class did not instantiate self._votes " \
                                                    "to an ndarray"
        assert isinstance(self._truths, np.ndarray), "specifics of implementing class did not instantiate " \
                                                     "self._truths to an ndarray"

    def get_bribers(self) -> Tuple[Any]:
        """
        Get the bribers active on the graph
        :return: the bribers
        """
        return self._bribers

    def get_max_rating(self) -> float:
        """
        Get the maximum rating
        :return: the maximum rating
        """
        return self._max_rating

    def set_rating_method(self, rating_method: RatingMethod):
        """
        Set the rating method being used
        :param rating_method: the rating method to use
        """
        self._rating_method = rating_method

    def get_rating(self, node_id: int = 0, briber_id: int = 0, rating_method: Optional[RatingMethod] = None, nan_default: Optional[int] = None):
        """
        Get the rating for a certain node and briber, according to the set rating method
        :param node_id: the node to find the rating of (can be omitted for O-rating)
        :param briber_id: the briber to find the rating of (can be omitted in single-briber rating graphs)
        :param rating_method: a rating method to override the current set rating method if not None
        :return: the rating
        """
        rm = rating_method or self._rating_method
        rating = np.nan
        if rm == RatingMethod.O_RATING:
            rating = self._o_rating(briber_id)
        elif rm == RatingMethod.P_RATING:
            rating = self._p_rating(node_id, briber_id)
        elif rm == RatingMethod.MEDIAN_P_RATING:
            rating = self._median_p_rating(node_id, briber_id)
        elif rm == RatingMethod.SAMPLE_P_RATING:
            rating = self._sample_p_rating(node_id, briber_id)
        elif rm == RatingMethod.WEIGHTED_P_RATING:
            rating = self._p_rating_weighted(node_id, briber_id)
        # elif rm == RatingMethod.PK_RATING:
        #     return self._pk_rating(node_id, briber_id)
        if np.isnan(rating) and nan_default: rating = nan_default
        return rating

    def graph(self):
        """
        Return the NetworKit graph of the network
        Ensure this information isn't used by a briber to "cheat"
        :return: the graph
        """
        return self._g

    def _neighbours(self, node_id: int, briber_id: int = 0) -> List[int]:
        """
        Get the voting neighbours of a node
        :param node_id: the node to get neighbours of
        :param briber_id: the briber on which voting has been done
        :return: the voting neighbours of the node for the briber
        """
        return [n for n in self._g.neighbors(node_id) if not np.isnan(self._votes[n][briber_id])]

    def get_customers(self) -> List[int]:
        """
        Get the customer ids without knowledge of edges or ratings
        :return: the customer ids in the graph
        """
        return list(self._g.nodes())

    def customer_count(self) -> int:
        """
        Get the number of customers
        :return: the number of nodes in the graph
        """
        return len(self._g.nodes())

    def get_vote(self, idx: int):
        """
        Returns the vote of a voter in the current network state
        :param idx: the id of the voter
        :return: np.nan if non-voter, otherwise float if single briber, np.ndarray of floats if multiple bribers
        """
        return self._votes[idx]

    def _p_rating(self, node_id: int, briber_id: int = 0):
        """
        Get the P-rating for the node
        :param node_id: the id of the node
        :param briber_id: the id number of the briber
        :param weighted: whether to weight nodes by trust
        :return: mean of actual rating of neighbouring voters
        """
        ns = self._neighbours(node_id, briber_id)
        if len(ns) == 0:
            return np.nan
        return sum(self.get_vote(n)[briber_id] for n in ns) / len(ns)

    def _p_rating_weighted(self, node_id: int, briber_id: int = 0):
        """
        Get the P-rating for the node, weighted based on trust
        :param node_id: the id of the node
        :param briber_id: the id number of the briber
        :return: mean of actual rating of neighbouring voters
        """
        ns = self._neighbours(node_id, briber_id)
        if len(ns) == 0:
            return np.nan
        dividing_factor = 0
        contributions = 0
        for n in ns:
            weight = self.get_weight(n, node_id)
            contributions += weight * self.get_vote(n)[briber_id]
            dividing_factor += weight
        return contributions / dividing_factor

    def _median_p_rating(self, node_id: int, briber_id: int = 0):
        """
        Get the median-based P-rating for the node
        :param node_id: the id of the node
        :param briber_id: the id number of the briber
        :return: median of actual rating of neighbouring voters
        """
        ns = self._neighbours(node_id, briber_id)
        ns = sorted(ns, key=lambda x: self.get_vote(x)[briber_id])
        return self.get_vote(ns[len(ns) // 2])[briber_id]

    def _sample_p_rating(self, node_id: int, briber_id: int = 0):
        """
        Get the sample-based P-rating for the node
        :param node_id: the id of the node
        :param briber_id: the id number of the briber
        :return: mean of a sample of actual rating of neighbouring voters
        """
        ns = self._neighbours(node_id, briber_id)
        sub = random.sample(ns, random.randint(1, len(ns)))
        return sum(self.get_vote(n)[briber_id] for n in sub) / len(sub)

    def _o_rating(self, briber_id: int = 0):
        """
        Get the O-rating for the node
        :param briber_id: the id number of the briber
        :return: mean of all actual ratings
        """
        ns = [n for n in self._g.nodes() if not np.isnan(self._votes[n][briber_id])]
        return sum(self.get_vote(n)[briber_id] for n in ns) / len(ns)
    
    def is_influential(self, node_id: int, k: float = 0.2, briber_id: int = 0,
                       rating_method: Optional[RatingMethod] = None, charge_briber: bool = True) -> float:
        """
        Determines if a node is influential using a small bribe
        :param node_id: the id of the node
        :param k: the cost of information
        :param briber_id: the briber for which the node may be influential
        :param rating_method: a rating method to override the current set rating method if not None
        :param charge_briber: whether this query is being made by a briber who must be charged and the ratings adjusted
        :return: float > 0 if influential, 0 otherwise
        """
        prev_p = self.eval_graph(briber_id, rating_method)
        vote = self.get_vote(node_id)[briber_id]
        if (not np.isnan(vote)) and (vote < 1 - k):
            if charge_briber:
                # bribe via the briber in order to charge their utility
                self._bribers[briber_id].bribe(node_id, k)
                reward = self.eval_graph(briber_id, rating_method) - prev_p - k
            else:
                # "bribe" directly on the graph, not charging the briber and not affecting ratings
                g_ = deepcopy(self)
                g_.bribe(node_id, k, briber_id)
                reward = g_.eval_graph(briber_id, rating_method) - prev_p - k
            if reward > 0:
                return reward
        return 0.0

    def bribe(self, node_id, b, briber_id=0):
        """
        Increase the rating of a node by an amount, capped at the max rating
        :param node_id: the node to bribe
        :param b: the amount to bribe the node
        :param briber_id: the briber who's performing the briber
        """
        if self._votes[node_id][briber_id]:
            self._votes[node_id][briber_id] = min(self._max_rating, self._votes[node_id][briber_id] + b)
        else:
            self._votes[node_id][briber_id] = min(self._max_rating, b)

    def eval_graph(self, briber_id=0, rating_method=None):
        """
        Metric to determine overall rating of the graph
        :param rating_method: a rating method to override the current set rating method if not None
        :return: the sum of the rating across the network
        :param briber_id: the briber being considered in the evaluation
        """
        return sum(self.get_rating(node_id=n, briber_id=briber_id, rating_method=rating_method, nan_default=0)
                   for n in self._g.nodes())
    
    def set_weight(self, node1_id: int, node2_id: int, weight: float):
        """
        Sets a weight for a given edge, thus allowing for trust metrics to affect graph structure.
        :param node1_id: the first node of the edge
        :param node2_id: the second node of the edge
        """
        self._g.setWeight(node1_id, node2_id, weight)
    
    def get_weight(self, node1_id: int, node2_id: int) -> float:
        """
        Gets the weight of a given edge.
        :param node1_id: the first node of the edge
        :param node2_id: the second node of the edge
        """
        return self._g.weight(node1_id, node2_id)
    
    def get_edges(self) -> [(int, int)]:
        return self._g.edges()
    
    def trust(self, node1_id: int, node2_id: int, rating_method: Optional[RatingMethod] = None) -> float:
        """
        Determines the trust of a given edge, which is a value from 0 to 1.
        This uses the average of the difference in rating between each pair of places.
        :param node1_id: the first node of the edge
        :param node2_id: the second node of the edge
        """
        se = 0
        # TODO: should loop over places instead of bribers, although right now these are equivalent
        for briber_id in range(len(self._bribers)):
            # Get ratings at each node, and take the square difference.
            diff = self.get_rating(node1_id, briber_id, rating_method) - self.get_rating(node2_id, briber_id, rating_method)
            if np.isnan(diff): diff = 0
            se += diff**2
        mse = se / len(self._bribers)
        return mse

    def __copy__(self):
        """
        copy operation.
        :return: A shallow copy of the instance
        """
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo=None):
        """
        deepcopy operation.
        :param memo: the memo dictionary
        :return: A deep copy of the instance
        """
        if memo is None:
            memo = {}
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            # noinspection PyArgumentList
            setattr(result, k, deepcopy(v, memo))
        return result
