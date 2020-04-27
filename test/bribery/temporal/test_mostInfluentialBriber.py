from copy import deepcopy

from bribery.temporal.mostInfluentialNodeBriber import MostInfluentialNodeBriber
from graph.temporal.noCustomerActionGraph import NoCustomerActionGraph
from test.bribery.temporal.briberTestCase import BriberTestCase
from unittest.mock import MagicMock

TEST_I = 7


class TestRandomBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = MostInfluentialNodeBriber(10, i=TEST_I)
        self.rg = NoCustomerActionGraph(self.briber)

    def test_next_action_increases_p_rating(self):
        graph = self.briber._g
        action = self.briber.next_action()
        briber_id = self.briber.get_briber_id()
        prev_eval = graph.eval_graph(briber_id=briber_id)

        action.perform_action()
        self.assertGreaterEqual(graph.eval_graph(briber_id=briber_id), prev_eval)

    def test_next_action_gains_information_for_suitable_time(self):
        prev_nodes = []
        for i in range(TEST_I - 1):
            action = self.briber.next_action()
            self.assertEqual(len(action._bribes), 1)
            for prev_node in prev_nodes:
                self.assertNotIn(prev_node, action._bribes)
            prev_nodes.append(self.briber._next_node)

    def test_next_action_performs_bribe_on_best_node(self):
        self.briber._c = self.briber._i
        self.briber._best_node = 1
        graph = self.briber._g
        graph.eval_graph = MagicMock(return_value=0)
        action = self.briber.next_action()
        self.assertIn(1, action._bribes)
        self.assertEqual(self.briber._c, 0)
        self.assertEqual(self.briber._max_rating_increase, 0)

    def test_next_action_finds_best_node(self):
        graph = self.briber._g
        graph.eval_graph = MagicMock(return_value=10)
        graph.get_random_customer = MagicMock(return_value=3)
        self.briber._previous_rating = 1
        self.briber._max_rating_increase = 0
        action = self.briber.next_action()
        self.assertIn(3, action._bribes)
        self.assertEqual(self.briber._max_rating_increase, 9)

    def test_next_action_does_not_fail_if_no_nodes_influential_within_i_step(self):
        graph = self.briber._g
        self.briber._previous_rating = 1
        graph.eval_graph = MagicMock(return_value=1)  # will never be influential
        prev_nodes = []
        for i in range(TEST_I + 1):
            action = self.briber.next_action()
            for prev_node in prev_nodes:
                self.assertNotIn(prev_node, action._bribes)
            prev_nodes.append(self.briber._next_node)

    def test_next_action_does_not_fail_if_no_nodes_influential_at_all(self):
        graph = self.briber._g
        self.briber._previous_rating = 1
        graph.eval_graph = MagicMock(return_value=1)  # will never be influential
        prev_nodes = []
        for i in range(graph.customer_count() + 1):
            action = self.briber.next_action()
            for prev_node in prev_nodes:
                self.assertNotIn(prev_node, action._bribes)
            prev_nodes.append(self.briber._next_node)
