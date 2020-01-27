from abc import ABC, abstractmethod

from bribery.briber import Briber
from bribery.temporal.briberyAction import BriberyAction


class TemporalBriber(Briber, ABC):

    def __init__(self, u0: float):
        super().__init__(u0=u0)

    @abstractmethod
    def next_action(self) -> BriberyAction:
        """
        Defines the temporal model behaviour
        """
        raise NotImplementedError
