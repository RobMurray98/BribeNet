# TODO: write composite graph generation.

from networkit.generators import BarabasiAlbertGenerator, WattsStrogatzGenerator
from networkit.graph import Graph
from random import gauss

def generate_composite_graph(n: int, community_count: int, small_world_conn: int, rewiring: float, scale_free_k: int):
    # First, generate a scale free network, which acts as our community network.
    communities = BarabasiAlbertGenerator(scale_free_k, community_count, 4, True).generate()
    small_world_graphs = {}
    nodes = communities.nodes()
    community_size = n / community_count
    # Then generate a small world graph for each node with size decided by a Gaussian distribution around the average node size.
    for i in range(len(nodes)-1, -1, -1):
        local_size = gauss(community_size, community_size / 3)
        local_n = min(round(local_size), n-i)
        if local_n <= 0: local_n = 1
        if i == 0: local_n = n
        small_world_graphs[nodes[i]] = WattsStrogatzGenerator(local_n, small_world_conn, rewiring).generate()
        n -= local_n
    # Build a merged graph.
    big_graph = Graph(0, False, False)
    ranges = [0]
    partition = []
    for graph in small_world_graphs:
        big_graph.append(graph)
        ranges.append(len(big_graph.nodes()))
        partition.append(list(range(ranges[-2], ranges[-1])))
    # Finally, connect these small world graphs where their parent nodes are connected.