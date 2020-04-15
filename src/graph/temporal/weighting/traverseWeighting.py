from networkit import Graph
import networkit as nk
from random import gauss

def assign_traverse_averaged(graph : Graph, mean : float, stdev : float=0.2) -> [float]:
    """
    Assign node 0 with the mean. Then assign all of its neighbours with a value
    close to that mean (weight + N(0, stdev)), then their neighbours and so on.
    By properties of normals, every node has weight ~ N(mean, x * (stdev**2))
    where x is the shortest distance from node 0, but nodes that are linked
    share very similar weights. Locally similar, globally variable.
    This version allows nodes with already assigned weights to be affected, by
    tracking each weight as a set and using its average.
    """
    weight_sets = [[] for i in graph.iterNodes()]
    weight_sets[0] = [mean]
    nodeset = [0]

    def average(l):
        return sum(l) / len(l)

    while len(nodeset) > 0:
        node = nodeset[0]
        nodeset = nodeset[1:]
        for neighbour in graph.neighbors(node):
            if len(weight_sets[neighbour]) == 0:
                nodeset.append(neighbour)
            weight_sets[neighbour].append(average(weight_sets[node]) + gauss(0, stdev))
    weights = [average(weight_sets[i]) for i in range(len(weight_sets))]
    avg_weight = sum(weights) / len(weights)
    return [min(1, max(0, weights[i] * mean / avg_weight)) for i in range(len(weights))]

def assign_traverse_weights(graph : Graph, mean : float, stdev : float=0.05) -> [float]:
    """
    Assign node 0 with the mean. Then assign all of its neighbours with a value
    close to that mean (weight + N(0, stdev)), then their neighbours and so on.
    By properties of normals, every node has weight ~ N(mean, x * (stdev**2))
    where x is the shortest distance from node 0, but nodes that are linked
    share very similar weights. Locally similar, globally variable.
    """
    weights = [-1 for i in graph.iterNodes()]
    weights[0] = mean
    nodeset = [0]
    while len(nodeset) > 0:
        node = nodeset[0]
        nodeset = nodeset[1:]
        for neighbour in graph.neighbors(node):
            if weights[neighbour] == -1:
                weights[neighbour] = weights[node] + gauss(0, stdev)
                nodeset.append(neighbour)
    avg_weight = sum(weights) / len(weights)
    return [min(1, max(0, weights[i] * mean / avg_weight)) for i in range(len(weights))]
