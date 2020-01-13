import random

from test.bribery.briberTestCase import BriberTestCase


class TestBriber(BriberTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_bribe(self):
        initial_u = self.briber.get_resources()
        bribe = random.randrange(0, initial_u)
        self.briber.bribe(0, bribe)
        self.assertEqual(self.briber.get_resources(), initial_u-bribe)
