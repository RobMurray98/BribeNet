from abc import ABC, abstractmethod
from unittest import TestCase

from bribery.static.nonBriber import NonBriber
from graph.static.ratingGraph import StaticRatingGraph


class BriberTestCase(TestCase, ABC):

    @abstractmethod
    def setUp(self) -> None:
        self.briber = NonBriber(1)
        self.rg = StaticRatingGraph(self.briber)

    def tearDown(self) -> None:
        del self.briber, self.rg

    def _p_rating_increase(self, g1, g2):
        rating2 = g2.eval_graph()
        rating1 = g1.eval_graph()
        self.assertGreater(rating2, rating1)
        return None
