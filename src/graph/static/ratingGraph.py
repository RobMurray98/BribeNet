from copy import deepcopy
import random
from typing import Tuple, Union

import numpy as np

from graph.ratingGraph import RatingGraph, DEFAULT_GEN
from helpers.override import override


class StaticRatingGraph(RatingGraph):
    from bribery.static.briber import StaticBriber

    def __init__(self, bribers: Union[Tuple[StaticBriber], StaticBriber], generator=DEFAULT_GEN, **kwargs):
        from bribery.static.briber import StaticBriber
        if issubclass(bribers.__class__, StaticBriber):
            bribers = tuple([bribers])
        assert isinstance(bribers, tuple), "bribers must be a tuple of instances of subclasses of StaticRatingBriber"
        assert len(bribers) > 0, "should be at least one briber"
        self.__tmp_bribers = bribers
        self.__tmp_kwargs = kwargs
        super().__init__(bribers, generator=generator, specifics=self.__specifics, **kwargs)

    @override
    def _finalise_init(self):
        """
        Perform assertions that ensure everything is initialised
        """
        super()._finalise_init()
        for briber in self._bribers:
            from bribery.static.briber import StaticBriber
            assert issubclass(briber.__class__, StaticBriber), "member of graph bribers not an instance of a " \
                                                               "subclass of StaticBriber"

    def __specifics(self):
        from bribery.static.briber import StaticBriber
        self._bribers: Tuple[StaticBriber] = self.__tmp_bribers
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
