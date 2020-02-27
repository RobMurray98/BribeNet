from abc import ABC, abstractmethod

from bribery.briber import Briber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction


class GraphNotSubclassOfTemporalRatingGraphException(Exception):
    pass


class TemporalBriber(Briber, ABC):

    def __init__(self, u0: float):
        super().__init__(u0=u0)

    def _set_graph(self, g):
        from graph.temporal.ratingGraph import TemporalRatingGraph
        if not issubclass(g.__class__, TemporalRatingGraph):
            raise GraphNotSubclassOfTemporalRatingGraphException(f"{g.__class__.__name__} is not a subclass of "
                                                                 "TemporalRatingGraph")
        super()._set_graph(g)

    def next_action(self) -> SingleBriberyAction:
        if self._g is None:
            raise BriberyGraphNotSetException()
        return self._next_action()

    @abstractmethod
    def _next_action(self) -> SingleBriberyAction:
        """
        Defines the temporal model behaviour
        """
        raise NotImplementedError
