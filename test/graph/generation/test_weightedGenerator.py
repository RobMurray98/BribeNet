from unittest import TestCase
from graph.generation.flatWeightGenerator import FlatWeightedGraphGenerator
from graph.generation import GraphGeneratorAlgo


class TestFlatWeightedGraphGenerator(TestCase):

    def test_generate_ws(self):
        graph_gen = FlatWeightedGraphGenerator(GraphGeneratorAlgo.WATTS_STROGATZ, 30, 5, 0.3)
        graph = graph_gen.generate()
        self.assertTrue(graph.isWeighted())

    def test_generate_ba(self):
        graph_gen = FlatWeightedGraphGenerator(GraphGeneratorAlgo.BARABASI_ALBERT, 5, 30, 0, True)
        graph = graph_gen.generate()
        self.assertTrue(graph.isWeighted())

    def test_generate_composite(self):
        graph_gen = FlatWeightedGraphGenerator(GraphGeneratorAlgo.COMPOSITE, 30, 15, 50, 0.1, 2)
        graph = graph_gen.generate()
        self.assertTrue(graph.isWeighted())
