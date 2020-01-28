from copy import deepcopy

from bribery.temporal.oneMoveRandomBriber import OneMoveRandomBriber
from graph.temporal.ratingGraph import TemporalRatingGraph
from test.bribery.temporal.briberTestCase import BriberTestCase


class TestOneMoveInfluentialNodeBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = OneMoveRandomBriber(10)
        # noinspection PyTypeChecker
        self.rg = TemporalRatingGraph(self.briber)

