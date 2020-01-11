from bribery.oneMoveINBriber import OneMoveINBriber
from graphGenerator import RatingGraph
from test.bribery.briberTestCase import BriberTestCase


class TestOneMoveINB(BriberTestCase):

    def setUp(self) -> None:
        self.briber = OneMoveINBriber(RatingGraph(), 10)

    def test_get_influencers(self):
        self.briber.get_influencers()
        self.assertTrue(len(self.briber.influencers) > 0)

    def test_next_bribe_increases_p_rating(self):
        initial_g = self.briber.g.copy()
        self.briber.next_bribe()
        self._p_rating_increase(initial_g, self.briber.g)
