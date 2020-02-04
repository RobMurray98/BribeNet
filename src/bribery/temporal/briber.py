from abc import ABC, abstractmethod

from bribery.briber import Briber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction


class TemporalBriber(Briber, ABC):

    def __init__(self, u0: float):
        super().__init__(u0=u0)

    @abstractmethod
    def next_action(self) -> SingleBriberyAction:
        """
        Defines the temporal model behaviour
        """
        raise NotImplementedError
