from copy import deepcopy
from unittest import TestCase

from graph.ratingGraph import RatingGraph


class TestRatingGraph(TestCase):

    def setUp(self) -> None:
        self.rating_graph = RatingGraph()
        self.__g = self.rating_graph.graph()

    def tearDown(self) -> None:
        del self.rating_graph

    def test_neighbors(self):
        for i in self.__g.nodes():
            ns = self.rating_graph._neighbours(i)
            self.assertTrue(len(ns) > 0)

    def test_p_rating(self):
        for i in self.__g.nodes():
            p = self.rating_graph._p_rating(i)
            self.assertTrue(p >= 0)

    def test_median_p_rating(self):
        for i in self.__g.nodes():
            p = self.rating_graph._median_p_rating(i)
            self.assertTrue(p >= 0)

    def test_sample_p_rating(self):
        for i in self.__g.nodes():
            p = self.rating_graph._sample_p_rating(i)
            self.assertTrue(p >= 0)

    def test_o_rating(self):
        self.assertTrue(self.rating_graph._o_rating())

    def test_bribe(self):
        initial_value = self.rating_graph.eval_graph()
        for i in self.__g.nodes():
            g_copy = deepcopy(self.rating_graph)
            g_copy.bribe(i, 0.1)
            bribed_value = g_copy.eval_graph()
            self.assertTrue(initial_value != bribed_value)
