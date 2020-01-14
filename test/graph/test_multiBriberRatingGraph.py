from copy import deepcopy
from unittest import TestCase

from bribery.nonBriber import NonBriber
from bribery.randomBriber import RandomBriber
from graph.multiBriberRatingGraph import MultiBriberRatingGraph


class TestMultiBriberRatingGraph(TestCase):

    def setUp(self) -> None:
        # noinspection PyTypeChecker
        self.rg = MultiBriberRatingGraph((RandomBriber(10), NonBriber(10)))

    def tearDown(self) -> None:
        del self.rg

    def test_neighbours(self):
        for i in range(len(self.rg.get_bribers())):
            for node in self.rg.get_customers():
                self.assertIsInstance(self.rg._neighbours(node, i), list)

    def test_p_rating(self):
        for b in range(len(self.rg.get_bribers())):
            for i in self.rg.get_customers():
                self.assertTrue(self.rg._p_rating(i, b) >= 0)

    def test_median_p_rating(self):
        for b in range(len(self.rg.get_bribers())):
            for i in self.rg.get_customers():
                self.assertTrue(self.rg._median_p_rating(i, b) >= 0)

    def test_sample_p_rating(self):
        for b in range(len(self.rg.get_bribers())):
            for i in self.rg.get_customers():
                self.assertTrue(self.rg._sample_p_rating(i, b) >= 0)

    def test_o_rating(self):
        for b in range(len(self.rg.get_bribers())):
            self.assertTrue(self.rg._o_rating(b) >= 0)

    def test_is_influential(self):
        for b in range(len(self.rg.get_bribers())):
            for i in self.rg.get_customers():
                self.assertIsInstance(self.rg.is_influential(i, 0.2, b), bool)

    def test_bribe(self):
        for i in range(len(self.rg.get_bribers())):
            initial_value = self.rg.eval_graph(i)
            for j in self.rg.get_customers():
                g_copy = deepcopy(self.rg)
                g_copy.bribe(j, 0.1, i)
                bribed_value = g_copy.eval_graph(i)
                self.assertTrue(initial_value != bribed_value)

    def test_eval_graph(self):
        for b in range(len(self.rg.get_bribers())):
            self.assertGreaterEqual(self.rg.eval_graph(b), 0)
