from unittest import TestCase

from BribeNet.bribery.static.influentialNodeBriber import InfluentialNodeBriber
from BribeNet.bribery.static.mostInfluentialNodeBriber import MostInfluentialNodeBriber
from BribeNet.bribery.static.nonBriber import NonBriber
from BribeNet.bribery.static.oneMoveInfluentialNodeBriber import OneMoveInfluentialNodeBriber
from BribeNet.bribery.static.oneMoveRandomBriber import OneMoveRandomBriber
from BribeNet.bribery.static.randomBriber import RandomBriber
from BribeNet.graph.static.ratingGraphBuilder import RatingGraphBuilder, BriberType


class TestRatingGraphBuilder(TestCase):

    def setUp(self) -> None:
        self.builder = RatingGraphBuilder()

    def tearDown(self) -> None:
        del self.builder

    def test_add_briber(self):
        classes = zip(BriberType._member_names_, [NonBriber, RandomBriber, OneMoveRandomBriber, InfluentialNodeBriber,
                                                  MostInfluentialNodeBriber, OneMoveInfluentialNodeBriber])
        for b, c in classes:
            self.builder.add_briber(getattr(BriberType, b), u0=10)
            self.assertIsInstance(self.builder.bribers[-1], c)

    def test_build_no_bribers(self):
        rg = self.builder.build()
        self.assertIsInstance(rg.get_bribers()[0], NonBriber)

    def test_build_one_briber(self):
        self.builder.add_briber(BriberType.Random)
        rg = self.builder.build()
        self.assertIsInstance(rg.get_bribers()[0], RandomBriber)

    def test_build_multiple_bribers(self):
        self.builder.add_briber(BriberType.Random).add_briber(BriberType.InfluentialNode)
        rg = self.builder.build()
        bribers = rg.get_bribers()
        self.assertEqual(len(bribers), 2)
        self.assertIsInstance(bribers[0], RandomBriber)
        self.assertIsInstance(bribers[1], InfluentialNodeBriber)
