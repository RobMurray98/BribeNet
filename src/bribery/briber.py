from abc import ABC, abstractmethod


class BriberyGraphNotSetException(Exception):
    pass


# abstract briber class
class Briber(ABC):
    def __init__(self, u0: float):
        self.__u = u0  # resources of briber to spend
        self.g = None  # network for agent
        self.max_rating = self.g.max_rating

    def set_graph(self, g):
        self.g = g

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
        pass
