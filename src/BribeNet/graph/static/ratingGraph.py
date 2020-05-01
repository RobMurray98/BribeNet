import random
from typing import Tuple, Union, Any

import numpy as np

from BribeNet.graph.ratingGraph import RatingGraph, DEFAULT_GEN, BribersAreNotTupleException, NoBriberGivenException
from BribeNet.helpers.override import override

DEFAULT_NON_VOTER_PROPORTION = 0.2


class BriberNotSubclassOfStaticBriberException(Exception):
    pass


class StaticRatingGraph(RatingGraph):

    def __init__(self, bribers: Union[Tuple[Any], Any], generator=DEFAULT_GEN, **kwargs):
        from BribeNet.bribery.static.briber import StaticBriber
        if issubclass(bribers.__class__, StaticBriber):
            bribers = tuple([bribers])
        if not isinstance(bribers, tuple):
            raise BribersAreNotTupleException()
        if not bribers:
            raise NoBriberGivenException()
        for b in bribers:
            if not issubclass(b.__class__, StaticBriber):
                raise BriberNotSubclassOfStaticBriberException(f"{b.__class__.__name__} is not a subclass of "
                                                               "StaticBriber")
        self.__tmp_bribers = bribers
        self.__tmp_kwargs = kwargs
        super().__init__(bribers, generator=generator, specifics=self.__specifics, **kwargs)

    @override
    def _finalise_init(self):
        """
        Perform assertions that ensure everything is initialised
        """
        from BribeNet.bribery.static.briber import StaticBriber
        for briber in self._bribers:
            if not issubclass(briber.__class__, StaticBriber):
                raise BriberNotSubclassOfStaticBriberException(f"{briber.__class__.__name__} is not a subclass of "
                                                               "StaticBriber")
        super()._finalise_init()

    def __specifics(self):
        from BribeNet.bribery.static.briber import StaticBriber
        self._bribers: Tuple[StaticBriber] = self.__tmp_bribers
        # noinspection PyTypeChecker
        self._votes = np.zeros((self.get_graph().numberOfNodes(), len(self._bribers)))
        self._truths = np.zeros((self.get_graph().numberOfNodes(), len(self._bribers)))
        # Generate random ratings network
        if "non_voter_proportion" in self.__tmp_kwargs:
            non_voter_proportion = self.__tmp_kwargs["non_voter_proportion"]
        else:
            non_voter_proportion = DEFAULT_NON_VOTER_PROPORTION
        for n in self.get_graph().iterNodes():
            for b, _ in enumerate(self._bribers):
                rating = random.uniform(0, self._max_rating)
                self._truths[n][b] = rating
                if random.random() > non_voter_proportion:
                    self._votes[n][b] = rating
                else:
                    self._votes[n][b] = np.nan
        del self.__tmp_bribers, self.__tmp_kwargs
