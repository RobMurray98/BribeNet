# noinspection PyUnresolvedReferences
from networkit import Graph
# noinspection PyUnresolvedReferences
from networkit.community import LPDegreeOrdered
import networkit as nk
import random


def get_communities(graph: Graph) -> [int]:
    communities = LPDegreeOrdered(graph).run().getPartition()
    return [communities.getMembers(i) for i in communities.getSubsetIds()]


def gauss_constrained(mean: float, std: float) -> float:
    return max(0, min(1, random.gauss(mean, std)))


# Generate a standard deviation based on the fraction of the total number
# of nodes in this particular community.
def get_stdev(total_size: int, comm_size: int) -> float:
    ratio = comm_size / total_size  # range 0 to 1.
    # We want a larger standard deviation for a smaller ratio.
    # Thus we take 1/ratio, which goes from total_size (for comm_size=1) to 1
    # (for ratio = 1). We divide this by total_size to get a normalised value,
    # and then by 3 so that we can easily reach three standard deviations
    # without leaving the range.
    return (1 / ratio) / (total_size * 3)


def assign_community_weights(graph: Graph, mean: float) -> [float]:
    weights = [0 for i in graph.nodes()]
    communities = get_communities(graph)
    total_size = len(weights)
    # For each community, assign it a mean and then give values within it a
    # normally distributed random value with that mean and standard dev
    # proportional to community size.
    for community in communities:
        comm_size = len(community)
        comm_mean = gauss_constrained(mean, 0.1)
        if comm_size == 1:
            weights[community[0]] = comm_mean
        else:
            for node in community:
                weights[node] = gauss_constrained(comm_mean, get_stdev(total_size, comm_size))
    return weights
