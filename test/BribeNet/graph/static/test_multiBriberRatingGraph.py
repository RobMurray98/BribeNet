from copy import deepcopy
from unittest import TestCase

from BribeNet.bribery.static.nonBriber import NonBriber
from BribeNet.bribery.static.randomBriber import RandomBriber
from BribeNet.graph.static.ratingGraph import StaticRatingGraph


class TestMultiBriberRatingGraph(TestCase):

    def setUp(self) -> None:
        # noinspection PyTypeChecker
        self.rg = StaticRatingGraph((RandomBriber(10), NonBriber(10)))

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

    def test_p_gamma_rating(self):
        for b in range(len(self.rg.get_bribers())):
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

    def test_o_rating(self):
        for b in range(len(self.rg.get_bribers())):
            rating = self.rg._o_rating(b)
            self.assertTrue(rating >= 0)

    def test_is_influential(self):
        for b in range(len(self.rg.get_bribers())):
            for i in self.rg.get_customers():
                self.assertGreaterEqual(self.rg.is_influential(i, 0.2, b, charge_briber=False), 0)

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
    
    def test_trust(self):
        for u in self.rg.get_customers():
            for v in self.rg.get_customers():
                trust1 = self.rg.trust(u, v)
                trust2 = self.rg.trust(v, u)
                self.assertEqual(trust1, trust2)
                self.assertGreaterEqual(trust1, 0)
                self.assertLessEqual(trust1, 1)
