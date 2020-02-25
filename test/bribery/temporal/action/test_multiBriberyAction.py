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
        try:
            action = MultiBriberyAction(self.graph)
            action.add_bribe(0, 0, -1.0)
        except BribeMustBeGreaterThanZeroException:
            return
        except Exception as e:
            self.fail(str(e))
        self.fail()

    def test_add_bribe_fails_if_node_id_not_present(self):
        try:
            action = MultiBriberyAction(self.graph)
            action.add_bribe(0, -1, 1.0)
        except NodeDoesNotExistException:
            return
        except Exception as e:
            self.fail(str(e))
        self.fail()

    def test_add_bribe_fails_if_briber_id_not_present_1(self):
        try:
            action = MultiBriberyAction(self.graph)
            action.add_bribe(-1, 0, 1.0)
        except BriberDoesNotExistException:
            return
        except Exception as e:
            self.fail(str(e))
        self.fail()

    def test_add_bribe_fails_if_briber_id_not_present_2(self):
        try:
            action = MultiBriberyAction(self.graph)
            action.add_bribe(4, 0, 1.0)
        except BriberDoesNotExistException:
            return
        except Exception as e:
            self.fail(str(e))
        self.fail()

    def test_add_bribe_passes_1(self):
        action = MultiBriberyAction(self.graph)
        action.add_bribe(0, 0, 1.0)
        self.assertEqual(action._bribes[0][0], 1.0)

    def test_add_bribe_passes_2(self):
        action = MultiBriberyAction(self.graph, bribes={0: {0: 1.0}})
        action.add_bribe(0, 0, 1.0)
        self.assertEqual(action._bribes[0][0], 2.0)

    def test__perform_action_fails_when_bribes_exceed_budget(self):
        try:
            action = MultiBriberyAction(self.graph, bribes={0: {0: 10.0}})
            action._perform_action()
        except BriberyActionExceedsAvailableUtilityException:
            return
        except Exception as e:
            self.fail(str(e))
        self.fail()

    def test_perform_action(self):
        try:
            action = MultiBriberyAction(self.graph, bribes=self.valid_action_dict)
            action._perform_action()
        except Exception as e:
            self.fail(str(e))

    def test_make_multi_action_from_single_actions_fails_if_on_different_graphs(self):
        try:
            other_briber = NonBriber(1)
            # noinspection PyUnusedLocal
            other_graph = NoCustomerActionGraph(other_briber)
            action0 = SingleBriberyAction(other_briber)
            action1 = SingleBriberyAction(self.bribers[0])
            MultiBriberyAction.make_multi_action_from_single_actions([action0, action1])
        except BriberyActionsOnDifferentGraphsException:
            return
        except Exception as e:
            self.fail(str(e))
        self.fail()

    def test_make_multi_action_from_single_actions_fails_if_no_actions(self):
        try:
            MultiBriberyAction.make_multi_action_from_single_actions([])
        except NoActionsToFormMultiActionException:
            return
        except Exception as e:
            self.fail(str(e))
        self.fail()

    def test_make_multi_action_from_single_actions_fails_if_bribe_not_greater_than_zero(self):
        try:
            action = SingleBriberyAction(self.bribers[0])
            action._bribes[0] = -1.0
            MultiBriberyAction.make_multi_action_from_single_actions([action])
        except BribeMustBeGreaterThanZeroException:
            return
        except Exception as e:
            self.fail(str(e))
        self.fail()

    def test_make_multi_action_from_single_actions_fails_if_at_different_times(self):
        try:
            action0 = SingleBriberyAction(self.bribers[0])
            action1 = SingleBriberyAction(self.bribers[1])
            action0.get_time_step = MagicMock(return_value=action0.get_time_step()+1)
            MultiBriberyAction.make_multi_action_from_single_actions([action0, action1])
        except BriberyActionsAtDifferentTimesException:
            return
        except Exception as e:
            self.fail(str(e))
        self.fail()

    def test_make_multi_action_from_single_actions(self):
        single_actions = [SingleBriberyAction(self.bribers[i], self.valid_action_dict[i])
                          for i in self.valid_action_dict.keys()]
        multi_action = MultiBriberyAction.make_multi_action_from_single_actions(single_actions)
        self.assertEqual(multi_action._bribes, self.valid_action_dict)
