from copy import deepcopy
from unittest import TestCase

from graph.singleBriberRatingGraph import SingleBriberRatingGraph


class TestRatingGraph(TestCase):

    def setUp(self) -> None:
        self.rg = SingleBriberRatingGraph(None)

    def tearDown(self) -> None:
        del self.rg

    def test_neighbors(self):
        for i in self.rg.graph().nodes():
            ns = self.rg._neighbours(i)
            self.assertTrue(len(ns) > 0)

    def test_p_rating(self):
        for i in self.rg.graph().nodes():
            p = self.rg._p_rating(i)
            self.assertTrue(p >= 0)

    def test_median_p_rating(self):
        for i in self.rg.graph().nodes():
            p = self.rg._median_p_rating(i)
            self.assertTrue(p >= 0)

    def test_sample_p_rating(self):
        for i in self.rg.graph().nodes():
            p = self.rg._sample_p_rating(i)
            self.assertTrue(p >= 0)

    def test_o_rating(self):
        self.assertTrue(self.rg._o_rating())

    def test_bribe(self):
        initial_value = self.rg.eval_graph()
        for i in self.rg.graph().nodes():
            g_copy = deepcopy(self.rg)
            g_copy.bribe(i, 0.1)
            bribed_value = g_copy.eval_graph()
            self.assertTrue(initial_value != bribed_value)
