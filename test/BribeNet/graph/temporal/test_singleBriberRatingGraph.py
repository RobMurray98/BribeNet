from copy import deepcopy
from unittest import TestCase

from BribeNet.bribery.temporal.nonBriber import NonBriber
from BribeNet.graph.temporal.noCustomerActionGraph import NoCustomerActionGraph


class TestSingleBriberRatingGraph(TestCase):

    def setUp(self) -> None:
        self.rg = NoCustomerActionGraph(NonBriber(0))

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

    def test_p_gamma_rating(self):
        for i in self.rg.get_customers():
            self.assertTrue(self.rg._p_gamma_rating(i) >= 0)
            self.assertAlmostEqual(self.rg._p_gamma_rating(i, gamma=0), self.rg._p_rating(i))

    def test_weighted_p_rating(self):
        for b in range(len(self.rg.get_bribers())):
            for i in self.rg.get_customers():
                self.assertTrue(self.rg._p_gamma_rating(i) >= 0)

    def test_weighted_median_p_rating(self):
        for b in range(len(self.rg.get_bribers())):
            for i in self.rg.get_customers():
                self.assertTrue(self.rg._p_gamma_rating(i) >= 0)
    
    def test_bribe(self):
        initial_value = self.rg.eval_graph()
        for i in self.rg.get_customers():
            g_copy = deepcopy(self.rg)
            g_copy.bribe(i, 0.1)
            bribed_value = g_copy.eval_graph()
            self.assertTrue(initial_value != bribed_value)
