from networkit.generators import WattsStrogatzGenerator
from numpy import logspace
from numpy import sum as npsum
from networkit.centrality import LocalClusteringCoefficient
from networkit.distance import APSP

trials = 5
inf = float("inf")

'''
Finds the clustering coefficient of a given graph.
'''
def average_clustering(graph, turbo=True):
    # If graphs get too large, turn off Turbo mode (which requires more memory)
    lcc = LocalClusteringCoefficient(graph, turbo)
    lcc.run()
    scores = lcc.scores()
    return sum(scores) / len(scores)

'''
Finds the average shortest path length of a given graph.
'''
def average_shortest_path_length(graph):
    apsp = APSP(graph)
    apsp.run()
    n = len(graph.nodes())
    # npsum needed as we are summing values in a matrix
    # Note! The matrix returned by getDistances is n*n, but we divide by n*n-1
    # since the central diagonal represents distances from a node to itself.
    return npsum(apsp.getDistances()) / (n*(n-1))

'''
Given an existing graph (from networkx), predict the parameters that should be used given.
Returns (n,k,p), where:
n: the number of nodes
k: the degree of nodes of the starting regular graph (that we rewire)
p: the probability of rewiring
'''
def predictSmallWorld(graph):
    n = len(graph.nodes())
    k = sum([len(graph.neighbors(i)) for i in graph.nodes()]) // (2*n)
    probs = logspace(-5, 0, 64, False, 10)
    (lvs, cvs, l0, c0) = generateExampleGraphs(n, k, probs)
    lp = average_shortest_path_length(graph)
    l_ratio = lp / l0
    cp = average_clustering(graph)
    c_ratio = cp / c0

    # Find the p according to l and c ratios
    index_l = closestIndex(lvs, l_ratio)
    index_c = closestIndex(cvs, c_ratio)
    prob_l = probs[index_l]
    prob_c = probs[index_c]

    p = (prob_l + prob_c) / 2
    return (n, k, p)

def closestIndex(values, target):
    mindiff = inf
    best = 0
    for i in range(len(values)):
        lv = values[i]
        diff = abs(lv - target)
        if diff < mindiff:
            best = i
            mindiff = diff
    return best

'''
For a set of p-values, generate existing WS graphs and get the values of L(p)/L(0) and C(p)/C(0).
Returns (lvals, cvals, l0, c0)
'''
def generateExampleGraphs(n, k, ps):
    generator0 = WattsStrogatzGenerator(n, k, 0)
    graph0 = generator0.generate()
    l0 = average_shortest_path_length(graph0)
    c0 = average_clustering(graph0)
    result = ([], [], l0, c0)
    for p in ps:
        l_tot = 0
        c_tot = 0
        generator = WattsStrogatzGenerator(n, k, p)
        for i in range(trials):
            graph = generator.generate()
            l_tot += average_shortest_path_length(graph)
            c_tot += average_clustering(graph)
        lp = l_tot / trials
        cp = c_tot / trials
        result[0].append(lp/l0)
        result[1].append(cp/c0)
    return result

if __name__ == '__main__':
    print("Testing with obviously Watts-Strogatz Graph (50,6,0.1)")
    generator = WattsStrogatzGenerator(50, 6, 0.1)
    print(predictSmallWorld(generator.generate()))