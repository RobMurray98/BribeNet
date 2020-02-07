from unittest import TestCase
from unittest.mock import MagicMock

from bribery.temporal.action.briberyAction import BriberyActionTimeNotCorrectException, \
    BriberyActionExecutedMultipleTimesException
from bribery.temporal.nonBriber import NonBriber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from graph.temporal.noCustomerActionGraph import NoCustomerActionGraph


class TestBriberyAction(TestCase):

    def setUp(self) -> None:
        self.briber = NonBriber(1)
        self.graph = NoCustomerActionGraph(self.briber)
        self.action = SingleBriberyAction(self.briber)

    def test_perform_action_fails_if_at_different_times(self):
        try:
            self.graph.get_time_step = MagicMock(return_value=self.action.get_time_step()+1)
            self.action.perform_action()
        except BriberyActionTimeNotCorrectException:
            return
        self.fail()

    def test_perform_action_fails_if_already_executed(self):
        try:
            self.action.add_bribe(0, 0.01)
            self.action.perform_action()
            self.action.perform_action()
        except BriberyActionExecutedMultipleTimesException:
            return
        self.fail()
