from unittest import TestCase

from BribeNet.bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from BribeNet.bribery.temporal.nonBriber import NonBriber
from BribeNet.graph.temporal.noCustomerActionGraph import NoCustomerActionGraph
from BribeNet.bribery.temporal.action import *


class TestSingleBriberyAction(TestCase):

    def setUp(self) -> None:
        self.briber = NonBriber(1)
        self.graph = NoCustomerActionGraph(self.briber)

    def test_add_bribe_fails_if_bribe_not_greater_than_zero(self):
        action = SingleBriberyAction(self.briber)
        self.assertRaises(BribeMustBeGreaterThanZeroException, action.add_bribe, 0, -1.0)

    def test_add_bribe_fails_if_node_id_not_present(self):
        action = SingleBriberyAction(self.briber)
        self.assertRaises(NodeDoesNotExistException, action.add_bribe, -1, 1.0)

    def test_add_bribe_passes_1(self):
        action = SingleBriberyAction(self.briber)
        action.add_bribe(0, 1.0)
        self.assertEqual(action._bribes[0], 1.0)

    def test_add_bribe_passes_2(self):
        action = SingleBriberyAction(self.briber, bribes={0: 1.0})
        action.add_bribe(0, 1.0)
        self.assertEqual(action._bribes[0], 2.0)

    def test__perform_action_fails_when_bribes_exceed_budget(self):
        action = SingleBriberyAction(self.briber, bribes={1: 10.0})
        self.assertRaises(BriberyActionExceedsAvailableUtilityException, action._perform_action)

    def test_perform_action(self):
        action = SingleBriberyAction(self.briber, bribes={0: 0.5})
        action.perform_action()
        self.assertTrue(action.get_performed())
