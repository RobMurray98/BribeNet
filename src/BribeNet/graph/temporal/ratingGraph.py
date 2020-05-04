import abc
import random
from sys import maxsize
from typing import Tuple, Union, Any, Optional, List

import numpy as np

from BribeNet.bribery.temporal.action.briberyAction import BriberyAction
from BribeNet.bribery.temporal.action.multiBriberyAction import MultiBriberyAction
from BribeNet.graph.ratingGraph import DEFAULT_GEN, RatingGraph, BribersAreNotTupleException, NoBriberGivenException
from BribeNet.graph.static.ratingGraph import DEFAULT_NON_VOTER_PROPORTION  # (0.2)
from BribeNet.graph.temporal.action.customerAction import CustomerAction
from BribeNet.graph.temporal.weighting.traverseWeighting import assign_traverse_averaged
from BribeNet.helpers.override import override

DEFAULT_REMOVE_NO_VOTE = False
DEFAULT_Q = 0.5
DEFAULT_PAY = 1.0
DEFAULT_APATHY = 0.0
DEFAULT_D = 2  # number of rounds in a cycle (D-1 bribes and then one customer round)
DEFAULT_TRUE_AVERAGE = 0.5
DEFAULT_TRUE_STD_DEV = 0.2
DEFAULT_LEARNING_RATE = 0.1

KWARG_NAMES = ("non_voter_proportion", "remove_no_vote", "q", "pay", "apathy", "d", "learning_rate")
KWARG_LOWER_BOUNDS = dict(zip(KWARG_NAMES, (0, False, 0, 0, 0, 2, 0)))
KWARG_UPPER_BOUNDS = dict(zip(KWARG_NAMES, (1, True, 1, float('inf'), 1, maxsize, 1)))


class BriberNotSubclassOfTemporalBriberException(Exception):
    pass


class BriberKeywordArgumentOutOfBoundsException(Exception):
    pass


class TrueAverageIncorrectShapeException(Exception):
    pass


class TrueStdDevIncorrectShapeException(Exception):
    pass


class TemporalRatingGraph(RatingGraph, abc.ABC):

    def __init__(self, bribers: Union[Tuple[Any], Any], generator=DEFAULT_GEN, **kwargs):
        from BribeNet.bribery.temporal.briber import TemporalBriber
        if issubclass(bribers.__class__, TemporalBriber):
            bribers = tuple([bribers])
        if not isinstance(bribers, tuple):
            raise BribersAreNotTupleException("bribers must be a tuple of instances of subclasses of TemporalBriber")
        if not bribers:
            raise NoBriberGivenException("must be at least one briber")
        for b in bribers:
            if not issubclass(b.__class__, TemporalBriber):
                raise BriberNotSubclassOfTemporalBriberException(f"{b.__class__.__name__} is not a subclass of "
                                                                 "TemporalBriber")
        self.__tmp_bribers = bribers
        self.__tmp_kwargs = kwargs
        self._time_step: int = 0
        super().__init__(bribers, generator, specifics=self.__specifics, **kwargs)
        # must come after super().__init__() such that bribers[0] has graph set
        if len(bribers) == 1:
            self._last_bribery_actions: List[BriberyAction] = []
            self._last_customer_action: Optional[CustomerAction] = CustomerAction.empty_action(self)
        else:
            self._last_bribery_actions: List[BriberyAction] = []
            self._last_customer_action: Optional[CustomerAction] = CustomerAction.empty_action(self)

    @staticmethod
    def kwarg_in_bounds(k, v):
        return KWARG_LOWER_BOUNDS[k] <= v <= KWARG_UPPER_BOUNDS[k]

    def __specifics(self):
        self._votes = np.zeros((self.get_graph().numberOfNodes(), len(self._bribers)))
        self._truths = np.zeros((self.get_graph().numberOfNodes(), len(self._bribers)))
        for kwarg in KWARG_NAMES:
            if kwarg in self.__tmp_kwargs:
                if not self.kwarg_in_bounds(kwarg, self.__tmp_kwargs[kwarg]):
                    raise BriberKeywordArgumentOutOfBoundsException(
                        f"{kwarg}={self.__tmp_kwargs[kwarg]} out of bounds ({KWARG_LOWER_BOUNDS[kwarg]}, "
                        f"{KWARG_UPPER_BOUNDS[kwarg]})")
        # Generate random ratings network
        if "non_voter_proportion" in self.__tmp_kwargs:
            non_voter_proportion = self.__tmp_kwargs["non_voter_proportion"]
        else:
            non_voter_proportion = DEFAULT_NON_VOTER_PROPORTION
        if "q" in self.__tmp_kwargs:
            self._q: float = self.__tmp_kwargs["q"] * self._max_rating
        else:
            self._q: float = DEFAULT_Q * self._max_rating
        if "pay" in self.__tmp_kwargs:
            self._pay: float = self.__tmp_kwargs["pay"]
        else:
            self._pay: float = DEFAULT_PAY
        if "apathy" in self.__tmp_kwargs:
            self._apathy: float = self.__tmp_kwargs["apathy"]
        else:
            self._apathy: float = DEFAULT_APATHY
        if "d" in self.__tmp_kwargs:
            self._d: int = self.__tmp_kwargs["d"]
        else:
            self._d: int = DEFAULT_D
        if "true_averages" in self.__tmp_kwargs:
            true_averages = self.__tmp_kwargs["true_averages"]
            if true_averages.shape[0] != len(self._bribers):
                raise TrueAverageIncorrectShapeException(f"{true_averages.shape[0]} != {len(self._bribers)}")
            self._true_averages: np.ndarray[float] = true_averages
        else:
            self._true_averages: np.ndarray[float] = np.repeat(DEFAULT_TRUE_AVERAGE, len(self._bribers))
        if "true_std_devs" in self.__tmp_kwargs:
            true_std_devs = self.__tmp_kwargs["true_std_devs"]
            if true_std_devs.shape[0] != len(self._bribers):
                raise TrueStdDevIncorrectShapeException(f"{true_std_devs.shape[0]} != {len(self._bribers)}")
            self._true_std_devs: np.ndarray[float] = true_std_devs
        else:
            self._true_std_devs: np.ndarray[float] = np.repeat(DEFAULT_TRUE_STD_DEV, len(self._bribers))
        if "learning_rate" in self.__tmp_kwargs:
            self._learning_rate: float = self.__tmp_kwargs["learning_rate"]
        else:
            self._learning_rate: float = DEFAULT_LEARNING_RATE
        community_weights = {}
        for b, _ in enumerate(self._bribers):
            community_weights[b] = assign_traverse_averaged(self.get_graph(), self._true_averages[b],
                                                            self._true_std_devs[b])
        for n in self.get_graph().iterNodes():
            for b, _ in enumerate(self._bribers):
                rating = community_weights[b][n]
                self._truths[n][b] = rating
                if random.random() > non_voter_proportion:
                    self._votes[n][b] = rating
                else:
                    self._votes[n][b] = np.nan
        self._time_step = 0
        del self.__tmp_bribers, self.__tmp_kwargs

    @override
    def _finalise_init(self):
        """
        Perform assertions that ensure everything is initialised
        """
        from BribeNet.bribery.temporal.briber import TemporalBriber
        for briber in self._bribers:
            if not issubclass(briber.__class__, TemporalBriber):
                raise BriberNotSubclassOfTemporalBriberException("member of graph bribers not an instance of a "
                                                                 "subclass of TemporalBriber")
        super()._finalise_init()

    def get_time_step(self):
        return self._time_step

    def get_d(self):
        return self._d

    def get_last_bribery_actions(self):
        return self._last_bribery_actions

    def get_last_customer_action(self):
        return self._last_customer_action

    @abc.abstractmethod
    def _customer_action(self) -> CustomerAction:
        """
        Perform the action of each customer in the graph
        """
        raise NotImplementedError

    def _bribery_action(self) -> MultiBriberyAction:
        actions = [b.next_action() for b in self._bribers]
        return MultiBriberyAction.make_multi_action_from_single_actions(actions)

    def _update_trust(self):
        """
        Update the weights of the graph based on the trust between nodes.
        """
        # Get the weights and calculate the new weights first.
        new_weights = {}
        for (u, v) in self.get_edges():
            prev_weight = self.get_weight(u, v)
            new_weight = prev_weight + self._learning_rate * (self.trust(u, v) - prev_weight)
            new_weights[(u, v)] = new_weight
        # Then set them, as some ratings systems could give different values
        # if the weights are modified during the calculations.
        for (u, v) in self.get_edges():
            self.set_weight(u, v, new_weights[(u, v)])

    def is_bribery_round(self):
        return not (self._time_step % self._d == self._d - 1)

    def step(self):
        """
        Perform the next step, either bribery action or customer action and increment the time step
        We do d-1 bribery steps (self._time_step starts at 0) and then a customer step.
        """
        if self.is_bribery_round():
            bribery_action = self._bribery_action()
            bribery_action.perform_action()
            self._last_bribery_actions.append(bribery_action)
        else:
            customer_action = self._customer_action()
            customer_action.perform_action(pay=self._pay)
            self._last_customer_action = customer_action
            self._last_bribery_actions = []
            self._update_trust()
        self._time_step += 1
