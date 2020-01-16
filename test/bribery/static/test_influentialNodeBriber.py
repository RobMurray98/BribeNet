from copy import deepcopy

from bribery.static.influentialNodeBriber import InfluentialNodeBriber
from graph.static.singleBriberRatingGraph import SingleBriberRatingGraph
from test.bribery.static.briberTestCase import BriberTestCase


class TestInfluentialNodeBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = InfluentialNodeBriber(10)
        self.rg = SingleBriberRatingGraph(self.briber)

    def test_next_bribe_increases_p_rating(self):
        initial_g = deepcopy(self.briber._g)
        self.briber.next_bribe()
        self._p_rating_increase(initial_g, self.briber._g)
