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

    def test__customer_action_runs(self):
        rg_copy = deepcopy(self.rg)
        self.rg.step()
        return
