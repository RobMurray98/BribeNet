from copy import deepcopy

from bribery.temporal.randomBriber import RandomBriber
from graph.temporal.ratingGraph import TemporalRatingGraph
from test.bribery.temporal.briberTestCase import BriberTestCase


class TestRandomBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = RandomBriber(10)
        self.rg = TemporalRatingGraph(self.briber)

    def test_next_action_increases_p_rating(self):
        graph = self.briber._g
        action = self.briber.next_action()
        briber_id = self.briber.get_briber_id()
        prev_eval = graph.eval_graph(briber_id=briber_id)

        action.perform_action()
        self.assertGreater(graph.eval_graph(briber_id=briber_id), prev_eval)