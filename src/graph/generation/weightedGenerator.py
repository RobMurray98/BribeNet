import abc

from graph.generation.generator import GraphGenerator
from graph.generation import GraphGeneratorAlgo, algo_to_constructor


class WeightedGraphGenerator(GraphGenerator, abc.ABC):

    def __init__(self, a: GraphGeneratorAlgo, *args, **kwargs):
        """
        Thin wrapper class for NetworKit graph generation algorithms which add weights to edges
        :param a: the GraphGenerationAlgo to use
        :param args: any arguments to this generator
        :param kwargs: any keyword arguments to this generator
        """
        super().__init__(a, *args, **kwargs)
