from abc import ABC, abstractmethod
from unittest import TestCase

from bribery.static.briber import StaticBriber
from graph.static.ratingGraph import StaticRatingGraph


class DummyBriber(StaticBriber):

    def next_bribe(self):
        pass

    def __init__(self, u0):
        super().__init__(u0)


class BriberTestCase(TestCase, ABC):

    @abstractmethod
    def setUp(self) -> None:
        self.briber = DummyBriber(10)
        self.rg = StaticRatingGraph(self.briber)

    def tearDown(self) -> None:
        del self.briber, self.rg

    def _p_rating_increase(self, g1, g2):
        rating2 = g2.eval_graph()
        rating1 = g1.eval_graph()
        self.assertTrue(rating2 > rating1)
        return None
