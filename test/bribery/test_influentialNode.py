from bribery.influentialNodeBriber import InfluentialNodeBriber
from graph.ratingGraph import RatingGraph
from test.bribery.briberTestCase import BriberTestCase


class TestInfluentialNodeBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = InfluentialNodeBriber(RatingGraph(), 10)

    def test_next_bribe_increases_p_rating(self):
        initial_g = self.briber._g.copy()
        self.briber.next_bribe()
        self._p_rating_increase(initial_g, self.briber._g)
