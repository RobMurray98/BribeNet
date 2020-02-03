import random
import numpy as np
from typing import Tuple, Union, Any

from graph.ratingGraph import RatingGraph, DEFAULT_GEN
from helpers.override import override

DEFAULT_NON_VOTER_PROPORTION = 0.2


class StaticRatingGraph(RatingGraph):

    def __init__(self, bribers: Union[Tuple[Any], Any], generator=DEFAULT_GEN, **kwargs):
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
        from bribery.static.briber import StaticBriber
        for briber in self._bribers:
            assert issubclass(briber.__class__, StaticBriber), "member of graph bribers not an instance of a " \
                                                               "subclass of StaticBriber"

    def __specifics(self):
        from bribery.static.briber import StaticBriber
        self._bribers: Tuple[StaticBriber] = self.__tmp_bribers
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
        del self.__tmp_bribers, self.__tmp_kwargs
