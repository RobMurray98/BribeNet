from graph.generation.generator import GraphGenerator
from graph.generation import GraphGeneratorAlgo, algo_to_constructor


class UnweightedGraphGenerator(GraphGenerator):

    def __init__(self, a: GraphGeneratorAlgo, *args, **kwargs):
        super().__init__(a, *args, **kwargs)

    def generate(self):
        generator = algo_to_constructor(self._algo)(*self._args, **self._kwargs)
        return generator.generate()
