from copy import deepcopy
from unittest import TestCase

from bribery.temporal.nonBriber import NonBriber
from bribery.temporal.randomBriber import RandomBriber
from graph.temporal.action.actionType import ActionType
from graph.temporal.thresholdGraph import ThresholdGraph
from unittest.mock import MagicMock


class TestThresholdGraph(TestCase):

    def setUp(self) -> None:
        self.rg = ThresholdGraph((NonBriber(10), NonBriber(10)), threshold=0.4, q=0.5)

    def tearDown(self) -> None:
        del self.rg

    def test_customer_action_runs_successfully(self):
        self.rg.step()
        self.rg.step()
        action = self.rg.get_last_customer_action()
        self.assertIsNotNone(action)
        self.assertTrue(action.get_performed())

    def test_customer_action_no_votes_runs_successfully(self):
        self.rg.get_rating = MagicMock(return_value=0)
        self.rg.step()
        self.rg.step()
        action = self.rg.get_last_customer_action()
        self.assertIsNotNone(action)
        for k in action._actions:
            self.assertNotEqual(action._actions[k], ActionType.SELECT)
        self.assertTrue(action.get_performed())

    def test_customer_action_disconnected_graph_runs_successfully(self):
        self.rg._neighbours = MagicMock(return_value=[])
        self.rg._q = 0.5
        self.rg.step()
        self.rg.step()
        action = self.rg.get_last_customer_action()
        self.assertIsNotNone(action)
        for k in action._actions:
            self.assertEqual(action._actions[k][0], ActionType.SELECT)
        self.assertTrue(action.get_performed())

    def test_customer_action_no_votes_with_remove_no_vote(self):
        self.rg.get_rating = MagicMock(return_value=0)
        self.rg._remove_no_vote = True
        self.rg.step()
        self.rg.step()
        action = self.rg.get_last_customer_action()
        self.assertIsNotNone(action)
        for k in action._actions:
            self.assertNotEqual(action._actions[k][0], ActionType.SELECT)
        self.assertTrue(action.get_performed())
