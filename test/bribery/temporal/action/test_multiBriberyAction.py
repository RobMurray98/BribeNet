from unittest import TestCase

from bribery.temporal.action.multiBriberyAction import MultiBriberyAction, BriberyActionsAtDifferentTimesException,\
    BriberyActionsOnDifferentGraphsException, NoActionsToFormMultiActionException
from bribery.temporal.action import *
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from bribery.temporal.nonBriber import NonBriber
from graph.temporal.noCustomerActionGraph import NoCustomerActionGraph
from unittest.mock import MagicMock


# noinspection PyBroadException
class TestMultiBriberyAction(TestCase):

    def setUp(self) -> None:
        self.bribers = (NonBriber(1), NonBriber(1), NonBriber(1), NonBriber(1))
        self.valid_action_dict = {0: {0: 0.5}, 2: {0: 0.5}, 3: {0: 0.5}}
        self.graph = NoCustomerActionGraph(self.bribers)

    def tearDown(self) -> None:
        del self.bribers, self.graph

    def test_add_bribe_fails_if_bribe_not_greater_than_zero(self):
        action = MultiBriberyAction(self.graph)
        self.assertRaises(BribeMustBeGreaterThanZeroException, action.add_bribe, 0, 0, -1.0)

    def test_add_bribe_fails_if_node_id_not_present(self):
        action = MultiBriberyAction(self.graph)
        self.assertRaises(NodeDoesNotExistException, action.add_bribe, 0, -1, 1.0)

    def test_add_bribe_fails_if_briber_id_not_present_1(self):
        action = MultiBriberyAction(self.graph)
        self.assertRaises(BriberDoesNotExistException, action.add_bribe, -1, 0, 1.0)

    def test_add_bribe_fails_if_briber_id_not_present_2(self):
        action = MultiBriberyAction(self.graph)
        self.assertRaises(BriberDoesNotExistException, action.add_bribe, 4, 0, 1.0)

    def test_add_bribe_passes_1(self):
        action = MultiBriberyAction(self.graph)
        action.add_bribe(0, 0, 1.0)
        self.assertEqual(action._bribes[0][0], 1.0)

    def test_add_bribe_passes_2(self):
        action = MultiBriberyAction(self.graph, bribes={0: {0: 1.0}})
        action.add_bribe(0, 0, 1.0)
        self.assertEqual(action._bribes[0][0], 2.0)

    def test_perform_action_fails_when_bribes_exceed_budget(self):
        action = MultiBriberyAction(self.graph, bribes={0: {0: 10.0}})
        self.assertRaises(BriberyActionExceedsAvailableUtilityException, action.perform_action)

    def test_perform_action(self):
        action = MultiBriberyAction(self.graph, bribes=self.valid_action_dict)
        action.perform_action()
        self.assertTrue(action.get_performed())

    def test_make_multi_action_from_single_actions_fails_if_on_different_graphs(self):
        other_briber = NonBriber(1)
        # noinspection PyUnusedLocal
        other_graph = NoCustomerActionGraph(other_briber)
        action0 = SingleBriberyAction(other_briber)
        action1 = SingleBriberyAction(self.bribers[0])
        self.assertRaises(BriberyActionsOnDifferentGraphsException,
                          MultiBriberyAction.make_multi_action_from_single_actions, [action0, action1])

    def test_make_multi_action_from_single_actions_fails_if_no_actions(self):
        self.assertRaises(NoActionsToFormMultiActionException,
                          MultiBriberyAction.make_multi_action_from_single_actions, [])

    def test_make_multi_action_from_single_actions_fails_if_bribe_not_greater_than_zero(self):
        action = SingleBriberyAction(self.bribers[0])
        action._bribes[0] = -1.0
        self.assertRaises(BribeMustBeGreaterThanZeroException,
                          MultiBriberyAction.make_multi_action_from_single_actions, [action])

    def test_make_multi_action_from_single_actions_fails_if_at_different_times(self):
        action0 = SingleBriberyAction(self.bribers[0])
        action1 = SingleBriberyAction(self.bribers[1])
        action0.get_time_step = MagicMock(return_value=action0.get_time_step()+1)
        self.assertRaises(BriberyActionsAtDifferentTimesException,
                          MultiBriberyAction.make_multi_action_from_single_actions, [action0, action1])

    def test_make_multi_action_from_single_actions(self):
        single_actions = [SingleBriberyAction(self.bribers[i], self.valid_action_dict[i])
                          for i in self.valid_action_dict.keys()]
        multi_action = MultiBriberyAction.make_multi_action_from_single_actions(single_actions)
        self.assertEqual(multi_action._bribes, self.valid_action_dict)
