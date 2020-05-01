from BribeNet.bribery.static.randomBriber import RandomBriber
from BribeNet.graph.static.ratingGraph import StaticRatingGraph
from test.bribery.static.briberTestCase import BriberTestCase


class TestRandomBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = RandomBriber(10)
        self.rg = StaticRatingGraph(self.briber)

    def test_next_bribe_does_not_exceed_budget(self):
        self.briber.next_bribe()
        self.assertTrue(self.briber.get_resources() >= 0)
