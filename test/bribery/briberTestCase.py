from abc import ABC, abstractmethod
from unittest import TestCase

from bribery.briber import Briber
from graph.singleBriberRatingGraph import SingleBriberRatingGraph


class DummyBriber(Briber):
    def __init__(self, g, u0):
        super().__init__(g, u0)


class BriberTestCase(TestCase, ABC):

    @abstractmethod
    def setUp(self) -> None:
        self.briber = DummyBriber(SingleBriberRatingGraph(), 10)

    def tearDown(self) -> None:
        del self.briber

    def _total_rating(self, g):
        return sum([x or 0 for x in [g.get_vote(c) for c in self.briber._g.get_customers()]])

    def _p_rating_increase(self, g1, g2):
        rating2 = self._total_rating(g2)
        rating1 = self._total_rating(g1)
        self.assertTrue(rating2 > rating1)
        return None
