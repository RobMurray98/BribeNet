import networkit.nxadapter as adap

# Networkit does not let you add weights to a previously unweighted graph.
# Thus we convert it to a Networkx graph, add weights and then revert.
def to_weighted(g):
    nxg = adap.nk2nx(g)

    for (u,v) in nxg.edges():
        nxg[u][v]['weight'] = 1.0

    return adap.nx2nk(nxg, 'weight')