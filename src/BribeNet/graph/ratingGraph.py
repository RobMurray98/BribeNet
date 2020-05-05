import random
from abc import ABC
from copy import deepcopy
from typing import Tuple, Optional, List, Any, Set

import networkit as nk
import numpy as np
from weightedstats import weighted_mean, weighted_median, mean, median

from BribeNet.graph.generation import GraphGeneratorAlgo
from BribeNet.graph.generation.flatWeightGenerator import FlatWeightedGraphGenerator
from BribeNet.graph.generation.generator import GraphGenerator
from BribeNet.graph.ratingMethod import RatingMethod
from BribeNet.helpers.bribeNetException import BribeNetException

DEFAULT_GEN = FlatWeightedGraphGenerator(GraphGeneratorAlgo.WATTS_STROGATZ, 30, 5, 0.3)
MAX_RATING = 1.0
MAX_DIFF = 0.6


class BribersAreNotTupleException(BribeNetException):
    pass


class NoBriberGivenException(BribeNetException):
    pass


class BriberNotSubclassOfBriberException(BribeNetException):
    pass


class VotesNotInstantiatedBySpecificsException(BribeNetException):
    pass


class TruthsNotInstantiatedBySpecificsException(BribeNetException):
    pass


class GammaNotSetException(BribeNetException):
    pass


class RatingGraph(ABC):
    """
    Representation of network graph which bribers interact with
    """

    def __init__(self, bribers: Tuple[Any], generator: GraphGenerator = DEFAULT_GEN, specifics=None,
                 **kwargs):
        """
        Abstract class for rating graphs
        :param bribers:   the bribing actors on the graph
        :param generator: the graph generator used to instantiate the graph
        :param specifics: function in implementing class to call after the superclass initialisation,
                          but prior to _finalise_init (template design pattern)
        :param **kwargs:  additional keyword arguments to the graph, such as max_rating
        """
        # Generate random ratings network
        self._g = generator.generate()
        from BribeNet.bribery.briber import Briber
        if issubclass(bribers.__class__, Briber):
            bribers = tuple([bribers])
        if not isinstance(bribers, tuple):
            raise BribersAreNotTupleException()
        if not bribers:
            raise NoBriberGivenException()
        for b in bribers:
            if not issubclass(b.__class__, Briber):
                raise BriberNotSubclassOfBriberException(f"{b.__class__.__name__} is not a subclass of Briber")
        self._bribers = bribers
        self._max_rating: float = MAX_RATING
        self._votes: np.ndarray[Optional[float]] = None
        self._truths: np.ndarray[float] = None
        self._rating_method: RatingMethod = RatingMethod.P_RATING
        self._gamma: Optional[float] = None
        if specifics is not None:
            specifics()
        self._finalise_init()

    def _finalise_init(self):
        """
        Perform assertions that ensure everything is initialised
        """
        if not isinstance(self._bribers, tuple):
            raise BribersAreNotTupleException("specifics of implementing class did not instantiate self._bribers "
                                              "as a tuple")
        from BribeNet.bribery.briber import Briber
        for briber in self._bribers:
            if not issubclass(briber.__class__, Briber):
                raise BriberNotSubclassOfBriberException(f"{briber.__class__.__name__} is not a subclass of Briber")
            # noinspection PyProtectedMember
            briber._set_graph(self)
        if not isinstance(self._votes, np.ndarray):
            raise VotesNotInstantiatedBySpecificsException()
        if not isinstance(self._truths, np.ndarray):
            raise TruthsNotInstantiatedBySpecificsException()

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

    def set_gamma(self, gamma: float):
        """
        Set gamma which is used as the dampening factor in P-gamma-rating
        :param gamma: the dampening factor in P-gamma-rating
        """
        self._gamma = gamma

    def get_rating(self, node_id: int = 0, briber_id: int = 0, rating_method: Optional[RatingMethod] = None,
                   nan_default: Optional[int] = None):
        """
        Get the rating for a certain node and briber, according to the set rating method
        :param node_id: the node to find the rating of (can be omitted for O-rating)
        :param briber_id: the briber to find the rating of (can be omitted in single-briber rating graphs)
        :param rating_method: a rating method to override the current set rating method if not None
        :param nan_default: optional default integer value to replace np.nan as default return
        :return: the rating
        """
        rating_method_used = rating_method or self._rating_method
        rating = np.nan
        if rating_method_used == RatingMethod.O_RATING:
            rating = self._o_rating(briber_id)
        elif rating_method_used == RatingMethod.P_RATING:
            rating = self._p_rating(node_id, briber_id)
        elif rating_method_used == RatingMethod.MEDIAN_P_RATING:
            rating = self._median_p_rating(node_id, briber_id)
        elif rating_method_used == RatingMethod.SAMPLE_P_RATING:
            rating = self._sample_p_rating(node_id, briber_id)
        elif rating_method_used == RatingMethod.WEIGHTED_P_RATING:
            rating = self._p_rating_weighted(node_id, briber_id)
        elif rating_method_used == RatingMethod.WEIGHTED_MEDIAN_P_RATING:
            rating = self._median_p_rating_weighted(node_id, briber_id)
        elif rating_method_used == RatingMethod.P_GAMMA_RATING:
            if self._gamma is None:
                raise GammaNotSetException()
            rating = self._p_gamma_rating(node_id, briber_id, self._gamma)
        if np.isnan(rating) and nan_default is not None:
            rating = nan_default
        return rating

    def get_graph(self):
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
        return [n for n in self.get_graph().neighbors(node_id) if not np.isnan(self._votes[n][briber_id])]

    def get_customers(self) -> List[int]:
        """
        Get the customer ids without knowledge of edges or ratings
        :return: the customer ids in the graph
        """
        return list(self.get_graph().iterNodes())

    def customer_count(self) -> int:
        """
        Get the number of customers
        :return: the number of nodes in the graph
        """
        return self.get_graph().numberOfNodes()

    def get_random_customer(self, excluding: Optional[Set[int]] = None) -> int:
        """
        Gets the id of a random customer
        :param excluding: set of customer ids not to be returned
        :return: random node id in the graph
        """
        if excluding is None:
            excluding = set()
        return random.choice(tuple(set(self.get_graph().iterNodes()) - excluding))

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
        :return: mean of actual rating of neighbouring voters
        """
        ns = self._neighbours(node_id, briber_id)
        if len(ns) == 0:
            return np.nan
        return mean([self.get_vote(n)[briber_id] for n in ns])

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
        weights = [self.get_weight(n, node_id) for n in ns]
        votes = [self.get_vote(n)[briber_id] for n in ns]
        return weighted_mean(votes, weights)

    def _median_p_rating(self, node_id: int, briber_id: int = 0):
        """
        Get the median-based P-rating for the node
        :param node_id: the id of the node
        :param briber_id: the id number of the briber
        :return: median of actual rating of neighbouring voters
        """
        ns = self._neighbours(node_id, briber_id)
        if len(ns) == 0:
            return np.nan
        return median([self.get_vote(n)[briber_id] for n in ns])

    def _median_p_rating_weighted(self, node_id: int, briber_id: int = 0):
        """
        Get the median-based P-rating for the node, weighted based on trust
        :param node_id: the id of the node
        :param briber_id: the id number of the briber
        :return: median of actual rating of neighbouring voters
        """
        ns = self._neighbours(node_id, briber_id)
        if len(ns) == 0:
            return np.nan
        weights = [self.get_weight(n, node_id) for n in ns]
        votes = [self.get_vote(n)[briber_id] for n in ns]
        return weighted_median(votes, weights)

    def _sample_p_rating(self, node_id: int, briber_id: int = 0):
        """
        Get the sample-based P-rating for the node
        :param node_id: the id of the node
        :param briber_id: the id number of the briber
        :return: mean of a sample of actual rating of neighbouring voters
        """
        ns = self._neighbours(node_id, briber_id)
        if len(ns) == 0:
            return np.nan
        sub = random.sample(ns, random.randint(1, len(ns)))
        return mean([self.get_vote(n)[briber_id] for n in sub])

    def _o_rating(self, briber_id: int = 0):
        """
        Get the O-rating for the node
        :param briber_id: the id number of the briber
        :return: mean of all actual ratings
        """
        ns = [n for n in self.get_graph().iterNodes() if not np.isnan(self._votes[n][briber_id])]
        if len(ns) == 0:
            return np.nan
        return mean([self.get_vote(n)[briber_id] for n in ns])

    def _p_gamma_rating(self, node_id: int, briber_id: int = 0, gamma: float = 0.05):
        """
        Get the P-gamma-rating for the node, which weights nodes based on the gamma factor:
        The gamma factor is defined as gamma^(D(n,c) - 1), where n is our starting node, c
        is the node we are considering and D(n,c) is the shortest distance.
        :param briber_id: the id number of the briber
        :return: weighted mean of all actual ratings based on the gamma factor
        """
        ns = [n for n in self._g.iterNodes() if (not np.isnan(self._votes[n][briber_id])) and n != node_id]
        # noinspection PyUnresolvedReferences
        unweighted_g = nk.graphtools.toUnweighted(self.get_graph())
        # noinspection PyUnresolvedReferences
        bfs_run = nk.distance.BFS(unweighted_g, node_id).run()
        distances = bfs_run.getDistances()
        weights = [gamma ** (distances[n] - 1) for n in ns]
        votes = [self.get_vote(n)[briber_id] for n in ns]
        return weighted_mean(votes, weights)

    def is_influential(self, node_id: int, k: float = 0.1, briber_id: int = 0,
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

    def _get_influence_weight(self, node_id: int, briber_id: Optional[int] = 0):
        """
        Get the influence weight of a node in the graph, as defined by Grandi
        and Turrini.
        :param node_id: the node to fetch the influence weight of
        :param briber_id: the briber (determines which neighbours have voted)
        :return: the influence weight of the node
        """
        neighbourhood_sizes = [len(self._neighbours(n, briber_id)) for n in self._neighbours(node_id, briber_id)]
        neighbour_weights = [1.0 / n for n in neighbourhood_sizes if n > 0]  # discard size 0 neighbourhoods
        return sum(neighbour_weights)

    def bribe(self, node_id, b, briber_id=0):
        """
        Increase the rating of a node by an amount, capped at the max rating
        :param node_id: the node to bribe
        :param b: the amount to bribe the node
        :param briber_id: the briber who's performing the briber
        """
        if not np.isnan(self._votes[node_id][briber_id]):
            self._votes[node_id][briber_id] = min(self._max_rating, self._votes[node_id][briber_id] + b)
        else:
            self._votes[node_id][briber_id] = min(self._max_rating, b)

    def eval_graph(self, briber_id=0, rating_method=None):
        """
        Metric to determine overall rating of the graph
        :param rating_method: a rating method to override the current set rating method if not None
        :param briber_id: the briber being considered in the evaluation
        :return: the sum of the rating across the network
        """
        return sum(self.get_rating(node_id=n, briber_id=briber_id, rating_method=rating_method, nan_default=0)
                   for n in self.get_graph().iterNodes())

    def average_rating(self, briber_id=0, rating_method=None):
        voting_customers = [c for c in self.get_graph().iterNodes() if not np.isnan(self.get_vote(c))[briber_id]]
        return self.eval_graph(briber_id, rating_method) / len(voting_customers)

    def set_weight(self, node1_id: int, node2_id: int, weight: float):
        """
        Sets a weight for a given edge, thus allowing for trust metrics to affect graph structure.
        :param node1_id: the first node of the edge
        :param node2_id: the second node of the edge
        :param weight: the weight of the edge to set
        """
        self.get_graph().setWeight(node1_id, node2_id, weight)

    def get_weight(self, node1_id: int, node2_id: int) -> float:
        """
        Gets the weight of a given edge.
        :param node1_id: the first node of the edge
        :param node2_id: the second node of the edge
        """
        return self.get_graph().weight(node1_id, node2_id)

    def get_edges(self) -> [(int, int)]:
        return list(self.get_graph().iterEdges())

    def trust(self, node1_id: int, node2_id: int) -> float:
        """
        Determines the trust of a given edge, which is a value from 0 to 1.
        This uses the average of the difference in vote between each pair of places.
        :param node1_id: the first node of the edge
        :param node2_id: the second node of the edge
        """
        votes1 = self.get_vote(node1_id)
        votes2 = self.get_vote(node2_id)
        differences = votes1 - votes2
        nans = np.isnan(differences)
        differences[nans] = 0
        differences = np.square(differences)
        trust = 1 - (np.sum(differences) / (len(differences) * MAX_DIFF ** 2))
        return max(0, min(1, trust))

    def average_trust(self):
        """
        Average trust value for all pairs of nodes
        """
        trusts = [self.get_weight(a, b)
                  for (a, b) in self.get_graph().iterEdges()]
        return np.mean(trusts)

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
