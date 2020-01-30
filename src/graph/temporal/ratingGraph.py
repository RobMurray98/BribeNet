import random
from typing import Tuple, Union, Any, Optional

import numpy as np

from bribery.temporal.action.briberyAction import BriberyAction
from bribery.temporal.action.multiBriberyAction import MultiBriberyAction
from graph.ratingGraph import DEFAULT_GEN, RatingGraph
from graph.temporal.decisionMethod import DecisionMethod
from helpers.override import override


class TemporalRatingGraph(RatingGraph):

    def __init__(self, bribers: Union[Tuple[Any], Any], generator=DEFAULT_GEN,
                 decision_method: DecisionMethod = DecisionMethod.THRESHOLD, **kwargs):
        from bribery.temporal.briber import TemporalBriber
        if issubclass(bribers.__class__, TemporalBriber):
            bribers = tuple([bribers])
        assert isinstance(bribers, tuple), "bribers must be a tuple of instances of subclasses of StaticRatingBriber"
        assert len(bribers) > 0, "should be at least one briber"
        for b in bribers:
            assert issubclass(b.__class__, TemporalBriber), "member of bribers tuple not an instance of a subclass " \
                                                            "of TemporalBriber"
        self.__tmp_bribers = bribers
        self.__tmp_kwargs = kwargs
        self._last_bribery_action: Optional[BriberyAction] = None
        self._time_step: int = 0
        self._decision_method = decision_method
        super().__init__(generator, specifics=self.__specifics, **kwargs)

    def __specifics(self):
        from bribery.temporal.briber import TemporalBriber
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

    def get_last_action(self):
        return self._last_bribery_action

    def _customer_action(self):
        """
        Perform the action of each customer in the graph
        """
        pass  # TODO (i30): implement threshold model

    def _bribery_action(self):
        actions = [b.next_action() for b in self._bribers]
        multi_action = MultiBriberyAction.make_multi_action_from_single_actions(actions)
        multi_action.perform_action()

    def step(self):
        """
        Perform the next step, either bribery action of customer action and increment the time step
        """
        if self._time_step % 2 == 0:
            self._bribery_action()
        else:
            self._customer_action()
        self._time_step += 1

