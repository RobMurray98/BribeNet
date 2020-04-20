from copy import deepcopy

from bribery.temporal.influentialNodeBriber import InfluentialNodeBriber
from graph.temporal.noCustomerActionGraph import NoCustomerActionGraph
from test.bribery.temporal.briberTestCase import BriberTestCase
from unittest.mock import MagicMock


class TestRandomBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = InfluentialNodeBriber(10)
        self.rg = NoCustomerActionGraph(self.briber)

    def test_next_action_increases_p_rating(self):
        graph = self.briber._g
        action = self.briber.next_action()
        briber_id = self.briber.get_briber_id()
        prev_eval = graph.eval_graph(briber_id=briber_id)

        action.perform_action()
        self.assertGreater(graph.eval_graph(briber_id=briber_id), prev_eval)

    def test_next_action_bribes_if_suitable(self):
        graph = self.briber._g
        self.briber._previous_rating = 0
        graph.eval_graph = MagicMock(return_value=1)
        graph.get_vote = MagicMock(return_value=[0.5])
        self.briber._next_node = 0
        action = self.briber.next_action()
        self.assertDictEqual(action._bribes, {0: 0.5})

    def test_next_action_moves_on_if_not_influential(self):
        graph = self.briber._g
        self.briber._previous_rating = 1
        graph.eval_graph = MagicMock(return_value=1)  # will never be influential
        prev_nodes = []
        for i in range(graph.customer_count()):
            action = self.briber.next_action()
            for prev_node in prev_nodes:
                self.assertNotIn(prev_node, action._bribes)
            prev_nodes.append(self.briber._next_node)

    def test_next_action_does_not_fail_if_no_nodes_influential(self):
        graph = self.briber._g
        self.briber._previous_rating = 1
        graph.eval_graph = MagicMock(return_value=1)  # will never be influential
        prev_nodes = []
        for i in range(graph.customer_count() + 1):
            action = self.briber.next_action()
            for prev_node in prev_nodes:
                self.assertNotIn(prev_node, action._bribes)
            prev_nodes.append(self.briber._next_node)

