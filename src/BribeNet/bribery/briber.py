from abc import ABC
from typing import Optional


class BriberyGraphNotSetException(Exception):
    pass


class BriberyGraphAlreadySetException(Exception):
    pass


class BriberNotRegisteredOnGraphException(Exception):
    pass


class GraphNotSubclassOfRatingGraphException(Exception):
    pass


class Briber(ABC):
    def __init__(self, u0: float):
        """
        Abstract class for bribing actors
        :param u0: the initial utility available to the briber
        """
        self._u = u0
        from BribeNet.graph.ratingGraph import RatingGraph
        self._g: Optional[RatingGraph] = None

    def _set_graph(self, g):
        from BribeNet.graph.ratingGraph import RatingGraph
        if not issubclass(g.__class__, RatingGraph):
            raise GraphNotSubclassOfRatingGraphException(f"{g.__class__.__name__} is not a subclass of RatingGraph")
        if self._g is not None:
            raise BriberyGraphAlreadySetException()
        self._g = g

    def get_graph(self):
        return self._g

    def get_briber_id(self):
        if self._g is None:
            raise BriberyGraphNotSetException()
        g_bribers = self._g.get_bribers()
        if issubclass(g_bribers.__class__, Briber):
            return 0
        for i, briber in enumerate(g_bribers):
            if briber is self:
                return i
        raise BriberNotRegisteredOnGraphException()

    def set_resources(self, u: float):
        self._u = u

    def add_resources(self, u: float):
        self._u += u

    def get_resources(self) -> float:
        return self._u

    def bribe(self, node_id: int, amount: float):
        if self._g is None:
            raise BriberyGraphNotSetException()
        if amount <= self._u:
            self._g.bribe(node_id, amount, self.get_briber_id())
            self._u -= amount
