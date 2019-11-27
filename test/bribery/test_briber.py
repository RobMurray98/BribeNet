import random

from test.bribery.briberTestCase import BriberTestCase


class TestBriber(BriberTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_bribe(self):
        initial_u = self.briber.u
        bribe = random.randrange(0, initial_u)
        self.briber.bribe(0, bribe)
        self.assertEqual(self.briber.u, initial_u-bribe)
