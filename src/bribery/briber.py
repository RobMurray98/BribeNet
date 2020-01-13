from abc import ABC, abstractmethod

from graph.ratingGraph import RatingGraph


class BriberyGraphNotSetException(Exception):
    pass


class BriberyGraphAlreadySetException(Exception):
    pass


# abstract briber class
class Briber(ABC):
    def __init__(self, u0: float):
        self._u = u0  # resources of briber to spend
        self._g = None  # network for agent

    def set_graph(self, g: RatingGraph):
        if self._g is not None:
            raise BriberyGraphAlreadySetException()
        self._g = g

    def set_resources(self, u: float):
        self._u = u

    def add_resources(self, u: float):
        self._u += u

    def get_resources(self) -> float:
        return self._u

    def bribe(self, bribe_id: int, amount: float):
        if self._g is None:
            raise BriberyGraphNotSetException()
        if amount <= self._u:
            self._g.bribe(bribe_id, amount)
            self._u -= amount

    @abstractmethod
    def next_bribe(self):
        raise NotImplementedError
