from unittest import TestCase
from BribeNet.graph.generation.unweightedGenerator import UnweightedGraphGenerator
from BribeNet.graph.generation import GraphGeneratorAlgo


class TestUnweightedGraphGenerator(TestCase):

    def test_generate_ws(self):
        graph_gen = UnweightedGraphGenerator(GraphGeneratorAlgo.WATTS_STROGATZ, 30, 5, 0.3)
        graph = graph_gen.generate()
        self.assertFalse(graph.isWeighted())

    def test_generate_ba(self):
        graph_gen = UnweightedGraphGenerator(GraphGeneratorAlgo.BARABASI_ALBERT, 5, 30, 0, True)
        graph = graph_gen.generate()
        self.assertFalse(graph.isWeighted())

    def test_generate_composite(self):
        graph_gen = UnweightedGraphGenerator(GraphGeneratorAlgo.COMPOSITE, 30, 15, 50, 0.1, 2)
        graph = graph_gen.generate()
        self.assertFalse(graph.isWeighted())
