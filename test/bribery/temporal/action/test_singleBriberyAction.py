from unittest import TestCase

from bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from bribery.temporal.nonBriber import NonBriber
from graph.temporal.ratingGraph import TemporalRatingGraph


class TestSingleBriberyAction(TestCase):

    def setUp(self) -> None:
        self.briber = NonBriber(1)
        self.graph = TemporalRatingGraph(self.briber)

    def test_add_bribe_fails_if_bribe_not_greater_than_zero(self):
        try:
            action = SingleBriberyAction(self.briber)
            action.add_bribe(0, -1.0)
        except AssertionError as e:
            self.assertEqual(str(e), "bribe quantity must be greater than 0")
            return
        self.fail()

    def test_add_bribe_fails_if_node_id_not_present(self):
        try:
            action = SingleBriberyAction(self.briber)
            action.add_bribe(-1, 1.0)
        except AssertionError as e:
            self.assertEqual(str(e), "node not present in graph")
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
            self.assertEqual(str(e), "SingleBriberyAction exceeded resources available to briber")
            return
        self.fail()

    def test__perform_action(self):
        try:
            action = SingleBriberyAction(self.briber, bribes={0: 0.5})
            action._perform_action()
        except Exception as e:
            self.fail(str(e))
