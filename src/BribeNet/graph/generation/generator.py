import abc

# noinspection PyUnresolvedReferences
from networkit import Graph

from BribeNet.graph.generation import GraphGeneratorAlgo, algo_to_constructor


class GraphGenerator(abc.ABC):

    def __init__(self, a: GraphGeneratorAlgo, *args, **kwargs):
        """
        Thin wrapper class for NetworKit graph generation algorithms
        :param a: the GraphGenerationAlgo to use
        :param args: any arguments to this generator
        :param kwargs: any keyword arguments to this generator
        """
        self._algo = a
        self._args = args
        self._kwargs = kwargs
        self._generator = algo_to_constructor(self._algo)(*args, **kwargs)

    @abc.abstractmethod
    def generate(self) -> Graph:
        """
        Call generate on the generator defined by this class and perform any additional actions
        :return: a NetworKit Graph
        """
        raise NotImplementedError
