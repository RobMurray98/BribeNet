from unittest import TestCase

from bribery.temporal.action.multiBriberyAction import MultiBriberyAction
from bribery.temporal.nonBriber import NonBriber
from graph.temporal.ratingGraph import TemporalRatingGraph


class TestMultiBriberyAction(TestCase):

    def setUp(self) -> None:
        self.bribers = (NonBriber(1), NonBriber(1), NonBriber(1), NonBriber(1))
        self.valid_action_dict = {0: {0: 0.5}, 2: {0: 0.5}, 3: {0: 0.5}}
        self.graph = TemporalRatingGraph(self.bribers)

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

    def test_add_bribe_passes_1(self):
        action = SingleBriberyAction(self.briber)
        action.add_bribe(0, 1.0)
        self.assertEqual(action.bribes[0], 1.0)

    def test_add_bribe_passes_2(self):
        action = SingleBriberyAction(self.briber, bribes={0: 1.0})
        action.add_bribe(0, 1.0)
        self.assertEqual(action.bribes[0], 2.0)

    def test__perform_action_fails_when_bribes_exceed_budget(self):
        try:
            action = SingleBriberyAction(self.briber, bribes={1: 10.0})
            action._perform_action()
        except AssertionError as e:
            self.assertEqual(str(e)[:6], "Single")
            return
        self.fail()

    def test__perform_action(self):
        try:
            action = MultiBriberyAction(self.briber, bribes={1: 0.5})
            action._perform_action()
        except Exception as e:
            self.fail(str(e))

    def test_make_multi_action_from_single_actions(self):
        self.fail()

    def test_add_bribe(self):
        self.fail()

    def test__perform_action(self):
        self.fail()
