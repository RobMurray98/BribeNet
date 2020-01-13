from copy import deepcopy

from bribery.influentialNodeBriber import InfluentialNodeBriber
from graph.singleBriberRatingGraph import SingleBriberRatingGraph
from test.bribery.briberTestCase import BriberTestCase


class TestInfluentialNodeBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = InfluentialNodeBriber(10)
        self.rg = SingleBriberRatingGraph(self.briber)
        self.briber.set_graph(self.rg)

    def test_next_bribe_increases_p_rating(self):
        initial_g = deepcopy(self.briber._g)
        self.briber.next_bribe()
        self._p_rating_increase(initial_g, self.briber._g)
