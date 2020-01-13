import enum
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Tuple, Optional, Union, List

import networkit as nk
import numpy as np

# noinspection PyUnresolvedReferences
DEFAULT_GEN = nk.generators.WattsStrogatzGenerator(30, 5, 0.3)


@enum.unique
class RatingMethod(enum.Enum):
    O_RATING = 0
    P_RATING = 1
    MEDIAN_P_RATING = 2
    SAMPLE_P_RATING = 3
    PK_RATING = 4


class RatingGraph(ABC):
    """
    Representation of network graph which bribers interact with
    """

    def __init__(self, generator=DEFAULT_GEN, specifics=None, **kwargs):
        """
        Implementing classes should initialise self.__true_rating and self.__bribers
        :param generator: the graph generator used to instantiate the graph
        """
        # Generate random ratings network
        self._g = generator.generate()
        self._bribers = None
        if "max_rating" in kwargs.keys():
            max_rating = kwargs["max_rating"]
        else:
            max_rating = 1.0
        self._max_rating: float = max_rating
        self._votes: np.ndarray[Optional[float]] = None
        self._rating_method: RatingMethod = RatingMethod.P_RATING
        if specifics is not None:
            specifics()
        self.__finalise_init()

    def __finalise_init(self):
        """
        Perform assertions that ensure everything is initialised
        """
        assert self._bribers is not None
        assert type(self._votes) is np.ndarray

    def set_rating_method(self, rating_method: RatingMethod):
        """
        Set the rating method being used
        :param rating_method: the rating method to use
        """
        self._rating_method = rating_method

    def get_rating(self, node_id: int = 0, briber_id: int = 0, rating_method: Optional[RatingMethod] = None):
        """
        Get the rating for a certain node and briber, according to the set rating method
        :param node_id: the node to find the rating of (can be omitted for O-rating)
        :param briber_id: the briber to find the rating of (can be omitted in single-briber rating graphs)
        :param rating_method: a rating method to override the current set rating method if not None
        :return: the rating
        """
        rm = rating_method or self._rating_method
        if rm == RatingMethod.O_RATING:
            return self._o_rating()
        if rm == RatingMethod.P_RATING:
            return self._p_rating(node_id, briber_id)
        if rm == RatingMethod.MEDIAN_P_RATING:
            return self._median_p_rating(node_id, briber_id)
        if rm == RatingMethod.SAMPLE_P_RATING:
            return self._sample_p_rating(node_id, briber_id)
        # if rm == RatingMethod.PK_RATING:
        #     return self._pk_rating(node_id, briber_id)

    def graph(self):
        """
        Return the NetworKit graph of the network
        Ensure this information isn't used by a briber to "cheat"
        :return: the graph
        """
        return self._g

    @abstractmethod
    def _neighbours(self, node_id: int, briber_id: int) -> List[int]:
        """
        Get the voting neighbours of a node
        :param node_id: the node to get neighbours of
        :param briber_id: the briber on which voting has been done
        :return: the voting neighbours of the node for the briber
        """
        raise NotImplementedError

    @abstractmethod
    def _p_rating(self, node_id: int, briber_id: int) -> float:
        """
        Get the P-rating for the node
        :param node_id: the id of the node
        :param briber_id: the id number of the briber
        :return: mean of actual rating of neighbouring voters
        """
        raise NotImplementedError

    @abstractmethod
    def _median_p_rating(self, node_id: int, briber_id: int) -> float:
        """
        Get the median-based P-rating for the node
        :param node_id: the id of the node
        :param briber_id: the id number of the briber
        :return: median of actual rating of neighbouring voters
        """
        raise NotImplementedError

    @abstractmethod
    def _sample_p_rating(self, node_id: int, briber_id: int) -> float:
        """
        Get the sample-based P-rating for the node
        :param node_id: the id of the node
        :param briber_id: the id number of the briber
        :return: mean of a sample of actual rating of neighbouring voters
        """
        raise NotImplementedError

    @abstractmethod
    def _o_rating(self) -> float:
        """
        Get the O-rating for the node
        :return: mean of all actual ratings
        """
        raise NotImplementedError

    def get_customers(self) -> List[int]:
        """
        Get the customer ids without knowledge of edges or ratings
        :return: the customer ids in the graph
        """
        return list(self._g.nodes())

    @abstractmethod
    def is_influential(self, node_id: int, k: float, briber_id: int, rating_method: Optional[RatingMethod]) -> bool:
        """
        Determines if a node is influential
        :param node_id: the id of the node
        :param k: the cost of information
        :param briber_id: the briber for which the node may be influential
        :param rating_method: a rating method to override the current set rating method if not None
        :return: True if influential, otherwise False
        """
        raise NotImplementedError

    def customer_count(self) -> int:
        """
        Get the number of customers
        :return: the number of nodes in the graph
        """
        return len(self._g.nodes())

    def get_vote(self, idx: int) -> Union[Optional[float], Tuple[Optional[float]]]:
        """
        Returns the true ratings of a voter in the current network state
        :param idx: the id of the voter
        :return: None if non-voter, otherwise float if single briber, tuple of floats if multiple bribers
        """
        return self._votes[idx]

    @abstractmethod
    def eval_graph(self, briber_id: int, rating_method: Optional[RatingMethod]) -> float:
        """
        Metric to determine overall rating of the graph
        :param rating_method: a rating method to override the current set rating method if not None
        :return: the sum of the rating across the network
        :param briber_id: the briber being considered in the evaluation
        """
        raise NotImplementedError

    @abstractmethod
    def bribe(self, node_id: int, b: float, briber_id: int):
        """
        Increase the rating of a node by an amount, capped at the max rating
        :param node_id: the node to bribe
        :param b: the amount to bribe the node
        :param briber_id: the briber who's performing the briber
        """
        raise NotImplementedError

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
