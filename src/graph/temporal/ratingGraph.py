import random
from typing import Tuple, Union, Any

import numpy as np

from bribery.temporal.action.multiBriberyAction import MultiBriberyAction
from graph.ratingGraph import DEFAULT_GEN, RatingGraph
from graph.static.ratingGraph import DEFAULT_NON_VOTER_PROPORTION
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
        self._decision_method = decision_method
        super().__init__(generator, specifics=self.__specifics, **kwargs)

    def __specifics(self):
        from bribery.temporal.briber import TemporalBriber
        self._bribers: Tuple[TemporalBriber] = self.__tmp_bribers
        # noinspection PyTypeChecker
        self._votes = np.zeros((len(self._g.nodes()), len(self._bribers)))
        self._truths = np.zeros((len(self._g.nodes()), len(self._bribers)))
        # Generate random ratings network
        if "non_voter_proportion" in self.__tmp_kwargs.keys():
            non_voter_proportion = self.__tmp_kwargs["non_voter_proportion"]
        else:
            non_voter_proportion = DEFAULT_NON_VOTER_PROPORTION
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

    def get_votes(self):
        return self._votes

    def _customer_action(self):
        """
        Perform the action of each customer in the graph
        """
        pass

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
