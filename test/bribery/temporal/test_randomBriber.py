from bribery.temporal.randomBriber import RandomBriber
from graph.temporal.ratingGraph import TemporalRatingGraph
from test.bribery.temporal.briberTestCase import BriberTestCase


class TestRandomBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = RandomBriber(10)
        self.rg = TemporalRatingGraph(self.briber)

    def test_next_bribe_does_not_exceed_budget(self):
        action = self.briber.next_action()
        # TODO