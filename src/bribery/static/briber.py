from abc import ABC

from bribery.briber import Briber, BriberyGraphAlreadySetException


class StaticBriber(Briber, ABC):

    def __init__(self, u0: float):
        super().__init__(u0=u0)

    def _set_graph(self, g):
        from graph.static.ratingGraph import StaticRatingGraph
        assert issubclass(g.__class__, StaticRatingGraph), "graph must be subclass of StaticRatingGraph"
        if self._g is not None:
            raise BriberyGraphAlreadySetException()
        self._g = g
