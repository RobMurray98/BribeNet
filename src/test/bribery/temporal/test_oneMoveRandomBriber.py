from BribeNet.bribery.temporal.oneMoveRandomBriber import OneMoveRandomBriber
from BribeNet.graph.temporal.noCustomerActionGraph import NoCustomerActionGraph
from test.bribery.temporal.briberTestCase import BriberTestCase


class TestOneMoveInfluentialNodeBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = OneMoveRandomBriber(10)
        self.rg = NoCustomerActionGraph(self.briber)

    def test_next_action_increases_p_rating(self):
        graph = self.briber._g
        action = self.briber.next_action()
        briber_id = self.briber.get_briber_id()
        prev_eval = graph.eval_graph(briber_id=briber_id)

        action.perform_action()
        self.assertGreaterEqual(graph.eval_graph(briber_id=briber_id), prev_eval)

