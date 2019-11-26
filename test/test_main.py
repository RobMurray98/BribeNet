import unittest

from bribery.influentialNode import InfluentialNodeBriber
from bribery.mostInfluencialNode import MostInfluentialNodeBriber
from bribery.random import RandomBriber
from graphGenerator import RatingGraph
from parameterPrediction import test_parameter_prediction


class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        self.rating_graph = RatingGraph()

    def tearDown(self) -> None:
        del self.rating_graph

    @staticmethod
    def graph_and_test(briber_setup, graph):
        print(graph.eval_graph())
        print("Bribing!")
        briber = briber_setup(graph)
        briber.next_bribe()
        print(graph.eval_graph())
        print("")

    def test_main(self):
        print("Testing parameter prediction!")
        test_parameter_prediction()
        print("")
        print("Testing random bribery on a graph!")
        self.graph_and_test(lambda g: RandomBriber(g, 10), self.rating_graph.copy())
        print("Testing influential node bribery on a graph!")
        self.graph_and_test(lambda g: InfluentialNodeBriber(g, 10, 0.2), self.rating_graph.copy())
        print("Testing most influential node bribery on a graph!")
        self.graph_and_test(lambda g: MostInfluentialNodeBriber(g, 10, 0.2), self.rating_graph.copy())
