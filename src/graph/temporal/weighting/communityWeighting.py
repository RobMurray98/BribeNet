import random

# noinspection PyUnresolvedReferences
from networkit import Graph
# noinspection PyUnresolvedReferences
from networkit.community import PLM


def get_communities(graph: Graph) -> [[int]]:
    """
    Gets the underlying communities of the graph, as sets of nodes.
    """
    communities = PLM(graph, refine=False).run().getPartition()
    return [communities.getMembers(i) for i in communities.getSubsetIds()]


def gauss_constrained(mean: float, std: float) -> float:
    return max(0, min(1, random.gauss(mean, std)))


def get_std_dev(total_size: int, comm_size: int) -> float:
    """
    In community generation, larger communities should have a smaller standard
    deviation (representing tighter-knit communities). This generates a std dev
    based on the ratio of the number of nodes in this community to the number
    of nodes in the total graph.

    Since we want a larger standard deviation for a smaller ratio, we take
    1/ratio, which goes from total_size (for comm_size=1) to 1 (for ratio = 1).
    We divide this by total_size to get a normalised value, and then by 3 so
    that we can easily go three standard deviations without leaving the range.
    """
    ratio = comm_size / total_size  # range 0 to 1.
    return (1 / ratio) / (total_size * 3)


def assign_community_weights(graph: Graph, mean: float, std_dev: float = 0.05) -> [float]:
    """
    For each community, assign it a mean and then give values within it a
    normally distributed random value with that mean and standard deviation
    proportional to community size.
    """
    weights = [0 for _ in graph.iterNodes()]
    communities = get_communities(graph)
    print(communities)
    total_size = len(weights)
    for community in communities:
        comm_size = len(community)
        comm_mean = gauss_constrained(mean, std_dev)
        if comm_size == 1:
            # noinspection PyTypeChecker
            # manually verified to be correct typing (rob)
            weights[community[0]] = comm_mean
        else:
            for node in community:
                # noinspection PyTypeChecker
                # manually verified to be correct typing (rob)
                weights[node] = gauss_constrained(comm_mean, get_std_dev(total_size, comm_size))
    return weights
