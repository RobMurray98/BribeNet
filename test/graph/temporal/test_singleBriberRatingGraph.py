from copy import deepcopy
from unittest import TestCase

from bribery.temporal.nonBriber import NonBriber
from graph.temporal.noCustomerActionGraph import NoCustomerActionGraph


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
            # NOTE: the below test doesn't actually work!
            # P-rating doesn't use the node itself, while O-rating does.
            # So these values will actually differ.
            # self.assertAlmostEqual(self.rg._p_gamma_rating(i, gamma=1), self.rg._o_rating())
    
    def test_bribe(self):
        initial_value = self.rg.eval_graph()
        for i in self.rg.get_customers():
            g_copy = deepcopy(self.rg)
            g_copy.bribe(i, 0.1)
            bribed_value = g_copy.eval_graph()
            self.assertTrue(initial_value != bribed_value)
