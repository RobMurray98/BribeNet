from copy import deepcopy

from bribery.temporal.randomBriber import RandomBriber
from graph.temporal.ratingGraph import TemporalRatingGraph
from test.bribery.temporal.briberTestCase import BriberTestCase


class TestRandomBriber(BriberTestCase):

    def setUp(self) -> None:
        self.briber = RandomBriber(10)
        # noinspection PyTypeChecker
        self.rg = TemporalRatingGraph(self.briber)