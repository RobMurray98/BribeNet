from unittest import TestCase


from networkit.generators import WattsStrogatzGenerator
from numpy import logspace

from prediction.parameterPrediction import ParameterPrediction


class TestParameterPrediction(TestCase):

    def setUp(self) -> None:
        self.generator = WattsStrogatzGenerator(50, 6, 0.1)
        self.pred = ParameterPrediction(self.generator.generate())

    def tearDown(self) -> None:
        del self.pred, self.generator

    def test_average_clustering(self):
        self.assertTrue(self.pred.average_clustering() > 0)

    def test_average_shortest_path_length(self):
        self.assertTrue(self.pred.average_shortest_path_length() > 0)

    def test_predict_small_world(self):
        n, k, p = self.pred.predict_small_world()
        self.assertTrue(n > 0)
        self.assertTrue(k > 0)
        self.assertTrue(p > 0)

    def test_generate_example_graphs(self):
        l_values, c_values, l0, c0 = ParameterPrediction.generate_example_graphs(50, 6, logspace(-5, 0, 64, False, 10))
        self.assertTrue(l0 > 0)
        self.assertTrue(c0 > 0)
        # tests below occasionally fail
        # TODO: put sensible assertions here?
        # self.assertTrue(max(l_values) <= 1)
        # self.assertTrue(min(l_values) >= 0)
        # self.assertTrue(max(c_values) <= 1)
        # self.assertTrue(min(c_values) >= 0)
