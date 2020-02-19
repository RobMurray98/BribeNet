from copy import deepcopy
from unittest import TestCase

from bribery.temporal.nonBriber import NonBriber
from bribery.temporal.randomBriber import RandomBriber
from graph.temporal.thresholdGraph import ThresholdGraph


class TestThresholdGraph(TestCase):

    def setUp(self) -> None:
        self.rg = ThresholdGraph((RandomBriber(10), NonBriber(10)))

    def tearDown(self) -> None:
        del self.rg

    def test_customer_action_runs_successfully(self):
        self.rg.step()
        self.rg.step()
        action = self.rg.get_last_customer_action()
        self.assertIsNotNone(action)
        self.assertTrue(action.get_performed())

    # TODO @nathan: further tests for unexplored paths through code
