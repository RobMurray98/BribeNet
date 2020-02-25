from unittest import TestCase

from bribery.temporal.action.multiBriberyAction import MultiBriberyAction
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from bribery.temporal.nonBriber import NonBriber
from graph.temporal.noCustomerActionGraph import NoCustomerActionGraph
from unittest.mock import MagicMock


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
        except AssertionError as e:
            self.assertEqual(str(e)[:5], "bribe")
            return
        self.fail()

    def test_add_bribe_fails_if_node_id_not_present(self):
        try:
            action = MultiBriberyAction(self.graph)
            action.add_bribe(0, -1, 1.0)
        except AssertionError as e:
            self.assertEqual(str(e)[:4], "node")
            return
        self.fail()

    def test_add_bribe_fails_if_briber_id_not_present_1(self):
        try:
            action = MultiBriberyAction(self.graph)
            action.add_bribe(-1, 0, 1.0)
        except AssertionError as e:
            self.assertEqual(str(e)[:6], "briber")
            return
        self.fail()

    def test_add_bribe_fails_if_briber_id_not_present_2(self):
        try:
            action = MultiBriberyAction(self.graph)
            action.add_bribe(4, 0, 1.0)
        except AssertionError as e:
            self.assertEqual(str(e)[:6], "briber")
            return
        self.fail()

    def test_add_bribe_passes_1(self):
        action = MultiBriberyAction(self.graph)
        action.add_bribe(0, 0, 1.0)
        self.assertEqual(action.bribes[0][0], 1.0)

    def test_add_bribe_passes_2(self):
        action = MultiBriberyAction(self.graph, bribes={0: {0: 1.0}})
        action.add_bribe(0, 0, 1.0)
        self.assertEqual(action.bribes[0][0], 2.0)

    def test__perform_action_fails_when_bribes_exceed_budget(self):
        try:
            action = MultiBriberyAction(self.graph, bribes={0: {0: 10.0}})
            action._perform_action()
        except AssertionError as e:
            self.assertEqual(str(e)[:57], "MultiBriberyAction exceeded resources available to briber")
            return
        self.fail()

    def test__perform_action(self):
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
        except AssertionError as e:
            self.assertEqual(str(e), "all actions must be on same graph")
            return
        self.fail()

    def test_make_multi_action_from_single_actions_fails_if_at_different_times(self):
        try:
            action0 = SingleBriberyAction(self.bribers[0])
            action1 = SingleBriberyAction(self.bribers[1])
            action0.get_time_step = MagicMock(return_value=action0.get_time_step()+1)
            MultiBriberyAction.make_multi_action_from_single_actions([action0, action1])
        except AssertionError as e:
            self.assertEqual(str(e), "all actions must be at same time")
            return
        self.fail()

    def test_make_multi_action_from_single_actions(self):
        single_actions = [SingleBriberyAction(self.bribers[i], self.valid_action_dict[i])
                          for i in self.valid_action_dict.keys()]
        multi_action = MultiBriberyAction.make_multi_action_from_single_actions(single_actions)
        self.assertEqual(multi_action.bribes, self.valid_action_dict)
