import enum

from networkit.generators import WattsStrogatzGenerator, BarabasiAlbertGenerator

from BribeNet.graph.generation.algo.compositeGenerator import CompositeGenerator
from BribeNet.helpers.bribeNetException import BribeNetException


class GraphGenerationAlgoNotDefinedException(BribeNetException):
    pass


@enum.unique
class GraphGeneratorAlgo(enum.Enum):
    """
    Enum of usable NetworKit graph generation algorithms
    """
    WATTS_STROGATZ = 0
    BARABASI_ALBERT = 1
    COMPOSITE = 2


def algo_to_constructor(g: GraphGeneratorAlgo):
    """
    Conversion method from an instance of the GraphGeneratorAlgo enum to a instantiable NetworKit generator class
    :param g: the algorithm
    :return: the relevant NetworKit generator class
    :raises GraphGenerationAlgoNotDefinedException: if g is not a member of the GraphGeneratorAlgo enum
    """
    if g == GraphGeneratorAlgo.WATTS_STROGATZ:
        return WattsStrogatzGenerator
    if g == GraphGeneratorAlgo.BARABASI_ALBERT:
        return BarabasiAlbertGenerator
    if g == GraphGeneratorAlgo.COMPOSITE:
        return CompositeGenerator
    # Add more algorithms here if needed
    raise GraphGenerationAlgoNotDefinedException(f"{g} is not a member of the GraphGeneratorAlgo enum")
