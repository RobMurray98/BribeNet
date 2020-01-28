from abc import ABC, abstractmethod
from copy import deepcopy
from unittest import TestCase

from bribery.temporal.nonBriber import NonBriber
from graph.temporal.ratingGraph import TemporalRatingGraph


class BriberTestCase(TestCase, ABC):

    @abstractmethod
    def setUp(self) -> None:
        self.briber = NonBriber(0)
        # noinspection PyTypeChecker
        self.rg = TemporalRatingGraph(self.briber)

    def tearDown(self) -> None:
        del self.briber, self.rg

    def test_next_action_increases_p_rating(self):
        graph = deepcopy(self.briber._g)
        action = self.briber.next_action()
        briber_id = self.briber.get_briber_id()
        prev_eval = graph.eval_graph(briber_id=briber_id)

        graph.bribe_action(action)
        self.assertGreater(graph.eval_graph(briber_id=briber_id), prev_eval)
