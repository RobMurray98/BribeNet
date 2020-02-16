import networkit as nk
import enum


class GraphGenerationAlgoNotDefinedException(Exception):
    pass


@enum.unique
class GraphGeneratorAlgo(enum.Enum):
    """
    Enum of usable NetworKit graph generation algorithms
    """
    WATTS_STROGATZ = 0
    BARABASI_ALBERT = 1


def algo_to_constructor(g: GraphGeneratorAlgo):
    """
    Conversion method from an instance of the GraphGeneratorAlgo enum to a instantiable NetworKit generator class
    :param g: the algorithm
    :return: the relevant NetworKit generator class
    :raises GraphGenerationAlgoNotDefinedException: if g is not a member of the GraphGeneratorAlgo enum
    """
    if g == GraphGeneratorAlgo.WATTS_STROGATZ:
        return nk.generators.WattsStrogatzGenerator
    if g == GraphGeneratorAlgo.BARABASI_ALBERT:
        return nk.generators.BarabasiAlbertGenerator
    # Add more algorithms here if needed
    raise GraphGenerationAlgoNotDefinedException(f"{g} is not a member of the GraphGeneratorAlgo enum")
