from unittest import TestCase
from BribeNet.bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from BribeNet.graph.temporal.action.customerAction import CustomerAction, CustomerActionExecutedMultipleTimesException,\
    CustomerActionTimeNotCorrectException
from BribeNet.bribery.temporal.nonBriber import NonBriber
from BribeNet.graph.temporal.noCustomerActionGraph import NoCustomerActionGraph
from BribeNet.graph.temporal.action.actionType import ActionType
from random import sample, randint, shuffle
from unittest.mock import MagicMock


class TestCustomerAction(TestCase):

    def setUp(self) -> None:
        self.briber = NonBriber(0)
        self.rg = NoCustomerActionGraph(self.briber)

    def test_set_bribed_from_bribery_action(self):
        nodes = self.rg.get_customers()
        for _ in range(10):
            customer_action = CustomerAction(self.rg)
            bribery_action = SingleBriberyAction(self.briber)
            bribed_nodes = sample(nodes, randint(1, len(nodes)))
            for bribed_node in bribed_nodes:
                bribery_action.add_bribe(bribed_node, 1.0)
            customer_action.set_bribed_from_bribery_action(bribery_action)
            bribed_in_customer_action = [c[0] for c in customer_action.actions.items() if c[1][0] == ActionType.BRIBED]
            self.assertEqual(set(bribed_in_customer_action), set(bribed_nodes))
            not_bribed_in_customer_action = [c[0] for c in customer_action.actions.items()
                                             if c[1][0] != ActionType.BRIBED]
            self.assertEqual(set(not_bribed_in_customer_action) & set(bribed_nodes), set())

    @staticmethod
    def __partition(list_in, n):
        shuffle(list_in)
        return [list_in[i::n] for i in range(n)]

    def test_perform_action_runs_normally(self):
        nodes = self.rg.get_customers()
        for _ in range(10):
            customer_action = CustomerAction(self.rg)
            partition = TestCustomerAction.__partition(nodes, 3)
            for n in partition[0]:
                customer_action.set_bribed(n, [0])
            for n in partition[1]:
                customer_action.set_select(n, 0)
            customer_action.perform_action(0)
            self.assertTrue(customer_action.get_performed())

    def test_perform_action_fails_when_time_incorrect(self):
        customer_action = CustomerAction(self.rg)
        self.rg.get_time_step = MagicMock(return_value=self.rg.get_time_step()+1)
        self.assertRaises(CustomerActionTimeNotCorrectException, customer_action.perform_action, 0)

    def test_perform_action_fails_when_executed_twice(self):
        customer_action = CustomerAction(self.rg)
        customer_action.perform_action(0)
        self.assertRaises(CustomerActionExecutedMultipleTimesException, customer_action.perform_action, 0)
