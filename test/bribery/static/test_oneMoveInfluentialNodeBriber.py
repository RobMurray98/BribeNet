from copy import deepcopy

from bribery.static.oneMoveInfluentialNodeBriber import OneMoveInfluentialNodeBriber
from graph.static.singleBriberRatingGraph import SingleBriberRatingGraph
from test.bribery.static.briberTestCase import BriberTestCase


class TestOneMoveInfluentialNodeBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = OneMoveInfluentialNodeBriber(10)
        self.rg = SingleBriberRatingGraph(self.briber)

    def test_get_influencers(self):
        self.briber.get_influencers()
        self.assertTrue(len(self.briber.influencers) > 0)

    def test_next_bribe_increases_p_rating(self):
        initial_g = deepcopy(self.briber._g)
        self.briber.next_bribe()
        self._p_rating_increase(initial_g, self.briber._g)
