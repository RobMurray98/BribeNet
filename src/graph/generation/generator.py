import abc
from graph.generation import GraphGeneratorAlgo
import networkit as nk


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

    @abc.abstractmethod
    def generate(self) -> nk.Graph:
        """
        Call generate on the generator defined by this class and perform any additional actions
        :return: a NetworKit Graph
        """
        raise NotImplementedError
