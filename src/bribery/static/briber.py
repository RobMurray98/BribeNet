from abc import ABC, abstractmethod

from bribery.briber import Briber, BriberyGraphAlreadySetException, BriberyGraphNotSetException


class StaticBriber(Briber, ABC):
    """
    Static bribers perform static bribery actions instantaneously on StaticRatingGraphs
    The abstract method next_bribe must be implemented to define the bribery action of the briber
    """

    def __init__(self, u0: float):
        super().__init__(u0=u0)

    def _set_graph(self, g):
        from graph.static.ratingGraph import StaticRatingGraph
        assert issubclass(g.__class__, StaticRatingGraph), "graph must be subclass of StaticRatingGraph"
        super()._set_graph(g)

    @abstractmethod
    def _next_bribe(self):
        """
        Statically perform some bribery action on the graph
        """
        raise NotImplementedError

    def next_bribe(self):
        if self._g is None:
            raise BriberyGraphNotSetException()
        self._next_bribe()
