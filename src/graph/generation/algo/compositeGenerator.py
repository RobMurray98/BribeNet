from math import floor
from random import gauss, sample, random

# noinspection PyUnresolvedReferences
from networkit import Graph
from networkit.generators import BarabasiAlbertGenerator, WattsStrogatzGenerator


class CompositeGenerator(object):
    """
    Pretend to extend inaccessible networkit._NetworKit.StaticGraphGenerator
    """

    def __init__(self, n: int, community_count: int, small_world_neighbours: int, rewiring: float,
                 scale_free_k: int, probability_reduce: float = 0.05):
        self._n = n
        self._community_count = community_count
        self._small_world_neighbours = small_world_neighbours
        self._rewiring = rewiring
        self._scale_free_k = scale_free_k
        self._probability_reduce = probability_reduce

    def generate(self):
        # First, generate a scale free network, which acts as our community network.
        communities = BarabasiAlbertGenerator(self._scale_free_k, self._community_count, 4, True).generate()
        small_world_graphs = {}
        nodes = communities.nodes()
        community_size = self._n / self._community_count
        # Then generate a small world graph for each node with size decided
        # by a Gaussian distribution around the average node size.
        for i in range(len(nodes) - 1, -1, -1):
            local_size = gauss(community_size, community_size / 3)
            local_n = min(round(local_size), self._n - i)
            # Cannot choose a local_n which is smaller than zero.
            if local_n <= 0:
                local_n = 1
            # If it's the last iteration, we much "use up" the rest of the nodes.
            if i == 0:
                local_n = self._n
            # There are many difficult parameters on connectivity,
            # which should be checked by NetworKit but currently they aren't.
            # As a result, we do the checks ourselves. (An issue has been filed.)
            connectivity = max(0, min(floor(local_n / 2) - 1, self._small_world_neighbours))
            small_world_graphs[nodes[i]] = WattsStrogatzGenerator(local_n, connectivity, self._rewiring).generate()
            self._n -= local_n
        # Build a merged graph.
        big_graph = Graph(0, False, False)
        ranges = [0]
        partition = []
        neighbours = [list(communities.neighbors(node)) for node in communities.nodes()]
        # To avoid neighbour sets having edges going both ways, delete references to nodes larger than themselves.
        for n in range(len(neighbours)):
            neighbours[n] = list(filter(lambda x: x < n, neighbours[n]))
        for graph in small_world_graphs.values():
            big_graph.append(graph)
            ranges.append(len(big_graph.nodes()))
            partition.append(list(range(ranges[-2], ranges[-1])))
        # Finally, connect these small world graphs where their parent nodes are connected.
        for i in range(len(neighbours)):
            for j in neighbours[i]:
                # Connect partitions i and j
                n1 = partition[i]
                n2 = partition[j]
                p = 1.0
                for nc1 in sample(n1, len(n1)):
                    for nc2 in sample(n2, len(n2)):
                        # Connect with probability p
                        if random() <= p:
                            big_graph.addEdge(nc1, nc2)
                            p = p * self._probability_reduce
        return big_graph


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from networkit.viztasks import drawGraph

    g = CompositeGenerator(4000, 15, 50, 0.1, 2).generate()
    drawGraph(g)
    plt.show()
