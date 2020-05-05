from abc import ABC, abstractmethod

from BribeNet.bribery.briber import Briber, BriberyGraphNotSetException
from BribeNet.bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from BribeNet.helpers.bribeNetException import BribeNetException


class GraphNotSubclassOfTemporalRatingGraphException(BribeNetException):
    pass


class TemporalBriber(Briber, ABC):

    def __init__(self, u0: float):
        super().__init__(u0=u0)

    def _set_graph(self, g):
        from BribeNet.graph.temporal.ratingGraph import TemporalRatingGraph
        if not issubclass(g.__class__, TemporalRatingGraph):
            raise GraphNotSubclassOfTemporalRatingGraphException(f"{g.__class__.__name__} is not a subclass of "
                                                                 "TemporalRatingGraph")
        super()._set_graph(g)

    def next_action(self) -> SingleBriberyAction:
        if self.get_graph() is None:
            raise BriberyGraphNotSetException()
        return self._next_action()

    @abstractmethod
    def _next_action(self) -> SingleBriberyAction:
        """
        Defines the temporal model behaviour
        """
        raise NotImplementedError
