from BribeNet.graph.generation import GraphGeneratorAlgo
from BribeNet.graph.generation.generator import GraphGenerator


class UnweightedGraphGenerator(GraphGenerator):

    def __init__(self, a: GraphGeneratorAlgo, *args, **kwargs):
        super().__init__(a, *args, **kwargs)

    def generate(self):
        return self._generator.generate()
