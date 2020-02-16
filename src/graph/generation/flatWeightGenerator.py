from graph.generation.weightedGenerator import WeightedGraphGenerator
from graph.generation import GraphGeneratorAlgo, algo_to_constructor


class FlatWeightedGraphGenerator(WeightedGraphGenerator):

    def __init__(self, a: GraphGenerationAlgo, *args, **kwargs):
        super().__init__(a, *args, **kwargs)

    def generate(self):
        # TODO @finnbar: move weight adding functionality here
        raise NotImplementedError
