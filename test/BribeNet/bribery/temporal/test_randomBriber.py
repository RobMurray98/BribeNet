from BribeNet.bribery.temporal.randomBriber import RandomBriber
from BribeNet.graph.temporal.noCustomerActionGraph import NoCustomerActionGraph
from test.BribeNet.bribery.temporal.briberTestCase import BriberTestCase


class TestRandomBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = RandomBriber(10)
        self.rg = NoCustomerActionGraph(self.briber)

    def test_next_action_increases_p_rating(self):
        graph = self.briber._g
        action = self.briber.next_action()
        briber_id = self.briber.get_briber_id()
        prev_eval = graph.eval_graph(briber_id=briber_id)

        action.perform_action()
        self.assertGreaterEqual(graph.eval_graph(briber_id=briber_id), prev_eval)
