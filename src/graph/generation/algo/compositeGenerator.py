from math import floor, log, ceil
from random import gauss, sample, random

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

    def _make_complete(self, n: int):
        g = nk.Graph(n)
        for i in g.iterNodes():
            for j in g.iterNodes():
                if i < j:
                    g.addEdge(i, j)
        return g

    def generate(self):
        # First, generate a scale free network, which acts as our community network.
        communities = BarabasiAlbertGenerator(self._scale_free_k, self._community_count, 4, True).generate()
        small_world_graphs = {}
        node_count = communities.numberOfNodes()
        community_size = self._n / self._community_count
        # Then generate a small world graph for each node with size decided
        # by a Gaussian distribution around the average node size.
        i = node_count - 1
        for node in communities.iterNodes():
            local_size = gauss(community_size, community_size / 3)
            # Choose local_n such that all communities have size at least two.
            local_n = min(round(local_size), self._n - (2 * i))
            # Cannot choose a local_n which is smaller than zero.
            if local_n <= 0:
                local_n = 1
            # If it's the last iteration, we much "use up" the rest of the nodes.
            if i == 0:
                local_n = self._n
            # For a random graph to be connected, we require that 2k >> ln(n).
            # (2k because of how NetworKit defines k.)
            # => k < (n-1)/2
            connectivity = max(self._small_world_neighbours, floor(log(local_n)))
            # However, we also require that 2k < n-1, since otherwise you end
            # up with double links.
            connectivity = max(0, min(ceil((local_n - 1) / 2) - 1, connectivity))
            if local_n > 3:
                small_world_graphs[node] = WattsStrogatzGenerator(local_n, connectivity, self._rewiring).generate()
            else:
                small_world_graphs[node] = self._make_complete(local_n)
            self._n -= local_n
            i -= 1
        # Build a merged graph.
        big_graph = Graph(0, False, False)
        ranges = [0]
        partition = []
        neighbours = [list(communities.neighbors(node)) for node in communities.iterNodes()]
        # To avoid neighbour sets having edges going both ways, delete references to nodes larger than themselves.
        for n in range(len(neighbours)):
            neighbours[n] = list(filter(lambda x: x < n, neighbours[n]))
        for graph in small_world_graphs.values():
            nk.graphtools.append(big_graph, graph)
            ranges.append(big_graph.numberOfNodes())
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
