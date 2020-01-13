from abc import ABC, abstractmethod

from graph.ratingGraph import RatingGraph


class BriberyGraphNotSetException(Exception):
    pass


# abstract briber class
class Briber(ABC):
    def __init__(self, g: RatingGraph, u0: float):
        self.__u = u0  # resources of briber to spend
        self.g = g  # network for agent
        self.max_rating = self.g._max_rating

    def set_resources(self, u: float):
        self.__u = u

    def add_resources(self, u: float):
        self.__u += u

    def bribe(self, bribe_id: int, amount: float):
        if self.g is None:
            raise BriberyGraphNotSetException()
        if amount <= self.__u:
            self.g.bribe(bribe_id, amount)
            self.__u -= amount

    @abstractmethod
    def next_bribe(self):
        raise NotImplementedError
