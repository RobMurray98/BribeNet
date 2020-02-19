import abc
import random
from typing import Tuple, Union, Any, Optional

import numpy as np

from bribery.temporal.action.briberyAction import BriberyAction
from bribery.temporal.action.multiBriberyAction import MultiBriberyAction
from graph.ratingGraph import DEFAULT_GEN, RatingGraph
from graph.static.ratingGraph import DEFAULT_NON_VOTER_PROPORTION
from graph.temporal.action.customerAction import CustomerAction
from helpers.override import override

DEFAULT_REMOVE_NON_VOTED = False
DEFAULT_Q = 0.5
DEFAULT_PAY = 1.0
DEFAULT_APATHY = 0.0


class TemporalRatingGraph(RatingGraph, abc.ABC):

    def __init__(self, bribers: Union[Tuple[Any], Any], generator=DEFAULT_GEN, **kwargs):
        from bribery.temporal.briber import TemporalBriber
        if issubclass(bribers.__class__, TemporalBriber):
            bribers = tuple([bribers])
        assert isinstance(bribers, tuple), "bribers must be a tuple of instances of subclasses of TemporalRatingBriber"
        assert len(bribers) > 0, "should be at least one briber"
        for b in bribers:
            assert issubclass(b.__class__, TemporalBriber), "member of bribers tuple not an instance of a subclass " \
                                                            "of TemporalBriber"
        self.__tmp_bribers = bribers
        self.__tmp_kwargs = kwargs
        self._last_bribery_action: Optional[BriberyAction] = None
        self._last_customer_action: Optional[BriberyAction] = None
        self._time_step: int = 0
        super().__init__(bribers, generator, specifics=self.__specifics, **kwargs)

    def __specifics(self):
        self._votes = np.zeros((len(self._g.nodes()), len(self._bribers)))
        self._truths = np.zeros((len(self._g.nodes()), len(self._bribers)))
        # Generate random ratings network
        if "non_voter_proportion" in self.__tmp_kwargs:
            non_voter_proportion = self.__tmp_kwargs["non_voter_proportion"]
        else:
            non_voter_proportion = DEFAULT_NON_VOTER_PROPORTION
        if "remove_non_voted" in self.__tmp_kwargs:
            self._remove_no_vote: bool = self.__tmp_kwargs["remove_non_voted"]
        else:
            self._remove_no_vote: bool = DEFAULT_REMOVE_NON_VOTED
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
        for n in self._g.nodes():
            for b, _ in enumerate(self._bribers):
                rating = random.uniform(0, self._max_rating)
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
        super()._finalise_init()
        from bribery.temporal.briber import TemporalBriber
        for briber in self._bribers:
            assert issubclass(briber.__class__, TemporalBriber), "member of graph bribers not an instance of a " \
                                                                 "subclass of TemporalBriber"

    def get_time_step(self):
        return self._time_step

    def get_last_bribery_action(self):
        return self._last_bribery_action

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

    def _update_trust(self, learning_rate: float = 0.1):
        """
        Update the weights of the graph based on the trust between nodes.
        :param learning_rate The learning rate at which we adjust our edge weights
        """
        # Get the weights and calculate the new weights first.
        new_weights = {}
        for (u, v) in self.get_edges():
            prev_weight = self.get_weight(u, v)
            new_weight = prev_weight + learning_rate * (self.trust(u, v) - prev_weight)
            new_weights[(u, v)] = new_weight
        # Then set them, as some ratings systems could give different values
        # if the weights are modified during the calculations.
        for (u, v) in self.get_edges():
            self.set_weight(u, v, new_weights[(u, v)])

    def step(self):
        """
        Perform the next step, either bribery action of customer action and increment the time step
        """
        if self._time_step % 2 == 0:
            bribery_action = self._bribery_action()
            bribery_action.perform_action()
            self._last_bribery_action = bribery_action
        else:
            customer_action = self._customer_action()
            customer_action.perform_action(pay=self._pay)
            self._last_customer_action = customer_action
            self._update_trust()
        self._time_step += 1
