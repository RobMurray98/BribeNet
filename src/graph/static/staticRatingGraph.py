from abc import ABC

from graph.ratingGraph import RatingGraph, DEFAULT_GEN

import numpy as np


class StaticRatingGraph(RatingGraph, ABC):

    def __init__(self, generator=DEFAULT_GEN, specifics=None, **kwargs):
        super().__init__(generator=generator, specifics=specifics, **kwargs)

    def __finalise_init(self):
        """
        Perform assertions that ensure everything is initialised
        """
        assert self.get_bribers() is not None, "specifics of implementing class did not instantiate self._bribers"
        from bribery.static.staticBriber import StaticBriber
        if issubclass(self.get_bribers().__class__, StaticBriber):
            # noinspection PyProtectedMember
            self._bribers._set_graph(self)
        else:
            assert isinstance(self.get_bribers(), tuple), "bribers on graph not instantiated as a tuple and not a " \
                                                          "single briber"
            for briber in self.get_bribers():
                assert issubclass(briber.__class__, StaticBriber), "member of graph bribers not an instance of a " \
                                                                   "subclass of StaticBriber"
                # noinspection PyProtectedMember
                briber._set_graph(self)
        assert type(self._votes) is np.ndarray, "specifics of implementing class did not instantiate self._votes to " \
                                                "an ndarray"
