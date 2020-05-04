from copy import deepcopy

from BribeNet.bribery.static.mostInfluentialNodeBriber import MostInfluentialNodeBriber
from BribeNet.graph.static.ratingGraph import StaticRatingGraph
from test.BribeNet.bribery.static.briberTestCase import BriberTestCase


class TestMostInfluentialNodeBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = MostInfluentialNodeBriber(10)
        self.rg = StaticRatingGraph(self.briber)

    def test_next_bribe_increases_p_rating(self):
        initial_g = deepcopy(self.briber._g)
        self.briber.next_bribe()
        self._p_rating_increase(initial_g, self.briber._g)
