from abc import ABC, abstractmethod
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

    def _total_rating(self, g):
        return sum([x or 0 for x in [g.get_vote(c) for c in self.briber._g.get_customers()]])

    def _p_rating_increase(self, g1, g2):
        rating2 = self._total_rating(g2)
        rating1 = self._total_rating(g1)
        self.assertTrue(rating2 > rating1)
        return None
