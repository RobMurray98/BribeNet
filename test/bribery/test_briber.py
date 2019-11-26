from unittest import TestCase

from bribery.briber import Briber
from graphGenerator import RatingGraph


class DummyBriber(Briber):
    def __init__(self, g, u0):
        super().__init__(g, u0)


class TestBriber(TestCase):

    def setUp(self) -> None:
        self.briber = DummyBriber(RatingGraph(), 10)

    def tearDown(self) -> None:
        del self.briber

    def test_bribe(self):
        # unimplemented test
        self.briber.bribe(0, 1)
        self.assertEqual(self.briber.u, 9)
