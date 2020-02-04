from abc import ABC, abstractmethod
from copy import deepcopy
from unittest import TestCase

from bribery.temporal.nonBriber import NonBriber
from graph.temporal.ratingGraph import TemporalRatingGraph


class BriberTestCase(TestCase, ABC):

    @abstractmethod
    def setUp(self) -> None:
        self.briber = NonBriber(0)
        self.rg = TemporalRatingGraph(self.briber)

    def tearDown(self) -> None:
        del self.briber, self.rg
