from copy import deepcopy
from unittest import TestCase

from graph.static.ratingGraph import StaticRatingGraph
from test.bribery.static.briberTestCase import DummyBriber


class TestSingleBriberRatingGraph(TestCase):

    def setUp(self) -> None:
        self.rg = StaticRatingGraph(DummyBriber(0))

    def tearDown(self) -> None:
        del self.rg

    def test_neighbors(self):
        for i in self.rg.get_customers():
            self.assertIsInstance(self.rg._neighbours(i), list)

    def test_p_rating(self):
        for i in self.rg.get_customers():
            self.assertTrue(self.rg._p_rating(i) >= 0)

    def test_median_p_rating(self):
        for i in self.rg.get_customers():
            self.assertTrue(self.rg._median_p_rating(i) >= 0)

    def test_sample_p_rating(self):
        for i in self.rg.get_customers():
            self.assertTrue(self.rg._sample_p_rating(i) >= 0)

    def test_o_rating(self):
        self.assertTrue(self.rg._o_rating() >= 0)

    def test_bribe(self):
        initial_value = self.rg.eval_graph()
        for i in self.rg.get_customers():
            g_copy = deepcopy(self.rg)
            g_copy.bribe(i, 0.1)
            bribed_value = g_copy.eval_graph()
            self.assertTrue(initial_value != bribed_value)
