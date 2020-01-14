from bribery.randomBriber import RandomBriber
from graph.singleBriberRatingGraph import SingleBriberRatingGraph
from test.bribery.briberTestCase import BriberTestCase


class TestOneMoveINB(BriberTestCase):

    def setUp(self) -> None:
        self.briber = RandomBriber(10)
        self.rg = SingleBriberRatingGraph(self.briber)

    def test_next_bribe_does_not_exceed_budget(self):
        self.briber.next_bribe()
        self.assertTrue(self.briber.get_resources() >= 0)
