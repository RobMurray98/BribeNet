from abc import ABC, abstractmethod

from bribery.briber import Briber


class TemporalBriber(Briber, ABC):

    def __init__(self, u0: float):
        super().__init__(u0=u0)

    @abstractmethod
    def step(self):
        """
        Defines the temporal model behaviour
        """
        raise NotImplementedError