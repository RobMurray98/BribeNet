import networkx as nx
from numpy import logspace
from networkx.algorithms import average_shortest_path_length, average_clustering

import matplotlib.pyplot as plt

trials = 5
inf = float("inf")

'''
Given an existing graph (from networkx), predict the parameters that should be used given.
Returns (n,k,p), where:
n: the number of nodes
k: the degree of nodes of the starting regular graph (that we rewire)
p: the probability of rewiring
'''
def predictSmallWorld(graph):
    n = len(graph.nodes)
    k = sum([len(graph.adj[i]) for i in graph.nodes]) // n
    probs = logspace(-5, 0, 256, False, 10)
    (lvs, cvs, l0, c0) = generateExampleGraphs(n, k, probs)
    plt.plot(probs, lvs)
    plt.show()
    plt.plot(probs, cvs)
    plt.show()
    lp = average_shortest_path_length(graph)
    l_ratio = lp / l0
    cp = average_clustering(graph)
    c_ratio = cp / c0
    print(l_ratio, c_ratio)

    # Find the p according to l and c ratios
    # The lookup is currently borked, investigate!
    # (looking at the graph, the values it predicts are correct but it's not getting them)
    index_l = closestIndex(lvs, l_ratio)
    index_c = closestIndex(cvs, c_ratio)
    prob_l = probs[index_l]
    prob_c = probs[index_c]
    print(prob_l, prob_c)

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
    graph0 = nx.watts_strogatz_graph(n, k, 0)
    l0 = average_shortest_path_length(graph0)
    c0 = average_clustering(graph0)
    result = ([], [], l0, c0)
    for p in ps:
        l_tot = 0
        c_tot = 0
        for i in range(trials):
            graph = nx.watts_strogatz_graph(n, k, p)
            l_tot += average_shortest_path_length(graph)
            c_tot += average_clustering(graph)
        lp = l_tot / trials
        cp = c_tot / trials
        result[0].append(lp/l0)
        result[1].append(cp/c0)
    return result

if __name__ == '__main__':
    print("Testing with obviously Watts-Strogatz Graph (50,6,0.1)")
    print(predictSmallWorld(nx.watts_strogatz_graph(50,6,0.1)))