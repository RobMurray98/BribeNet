from graph.generation.weightedGenerator import WeightedGraphGenerator
from graph.generation import GraphGeneratorAlgo, algo_to_constructor
import networkit.nxadapter as adap
import networkit as nk

class FlatWeightedGraphGenerator(WeightedGraphGenerator):

    def __init__(self, a: GraphGeneratorAlgo, *args, **kwargs):
        super().__init__(a, *args, **kwargs)

    # Networkit does not let you add weights to a previously unweighted graph.
    # Thus we convert it to a Networkx graph, add weights and then revert.
    def generate(self) -> nk.graph:
        nxg = adap.nk2nx(self._algo.generate())

        for (u,v) in nxg.edges():
            nxg[u][v]['weight'] = 1.0

        return adap.nx2nk(nxg, 'weight')
