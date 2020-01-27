from copy import deepcopy

from bribery.temporal.oneMoveRandomBriber import OneMoveRandomBriber
from graph.temporal.ratingGraph import TemporalRatingGraph
from test.bribery.temporal.briberTestCase import BriberTestCase


class TestOneMoveInfluentialNodeBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = OneMoveRandomBriber(10)
        self.rg = TemporalRatingGraph(self.briber)

    def test_next_action_increases_p_rating(self):
        initial_g = deepcopy(self.briber._g)
        action = self.briber.next_action()
        # TODO
