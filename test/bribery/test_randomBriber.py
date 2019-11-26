from bribery.random import RandomBriber
from graphGenerator import RatingGraph
from test.bribery.briberTestCase import BriberTestCase


class TestOneMoveINB(BriberTestCase):

    def setUp(self) -> None:
        self.briber = RandomBriber(RatingGraph(), 10)

    def test_next_bribe_does_not_exceed_budget(self):
        self.briber.next_bribe()
        self.assertTrue(self.briber.u >= 0)
