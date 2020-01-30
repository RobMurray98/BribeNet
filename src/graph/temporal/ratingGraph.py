import random
from typing import Tuple, Union, Any

import numpy as np

from bribery.temporal.action.briberyAction import BriberyAction
from graph.ratingGraph import DEFAULT_GEN, RatingGraph
from helpers.override import override


class TemporalRatingGraph(RatingGraph):

    def __init__(self, bribers: Union[Tuple[Any], Any], generator=DEFAULT_GEN, **kwargs):
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
        self.time_step: int = 0
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

    def bribe_action(self, action: BriberyAction):
        """
        Perform a bribery action and increment the time step
        :param action: the bribery action to be performed
        """
        action.perform_action()
        self.time_step += 1

    def get_time_step(self):
        return self.time_step

    def step(self):
        # TODO: implement temporal model behaviour
        raise NotImplementedError
