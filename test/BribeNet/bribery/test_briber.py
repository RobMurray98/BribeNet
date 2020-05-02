import random

from test.BribeNet.bribery.static.briberTestCase import BriberTestCase
from BribeNet.bribery.briber import BriberyGraphAlreadySetException, BriberyGraphNotSetException
from BribeNet.bribery.static.nonBriber import NonBriber


class TestBriber(BriberTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_bribe(self):
        initial_u = self.briber.get_resources()
        bribe = random.randrange(0, initial_u)
        self.briber.bribe(0, bribe)
        self.assertEqual(self.briber.get_resources(), initial_u-bribe)

    def test_next_bribe_fails_if_graph_not_set(self):
        briber = NonBriber(0)
        self.assertRaises(BriberyGraphNotSetException, briber.next_bribe)

    def test_set_graph_fails_if_graph_already_set(self):
        self.assertRaises(BriberyGraphAlreadySetException, self.briber._set_graph, self.rg)
