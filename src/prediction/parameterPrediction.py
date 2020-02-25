
from networkit.generators import WattsStrogatzGenerator
from numpy import logspace
from numpy import sum as np_sum

from networkit.centrality import LocalClusteringCoefficient

from networkit.distance import APSP

TRIALS = 5
INFINITY = float("inf")

# TODO: Implement for scale-free.

'''
Finds the clustering coefficient of a given graph.
'''


class ParameterPrediction(object):

    def __init__(self, graph):
        self.__g = graph

    def average_clustering(self, turbo=True):
        # If graphs get too large, turn off Turbo mode (which requires more memory)
        lcc = LocalClusteringCoefficient(self.__g, turbo)
        lcc.run()
        scores = lcc.scores()
        return sum(scores) / len(scores)

    '''
    Finds the average shortest path length of a given graph.
    '''

    def average_shortest_path_length(self):
        apsp = APSP(self.__g)
        apsp.run()
        n = len(self.__g.nodes())
        # npsum needed as we are summing values in a matrix
        # Note! The matrix returned by getDistances is n*n, but we divide by n*n-1
        # since the central diagonal represents distances from a node to itself.
        distances = apsp.getDistances()
        return np_sum(distances) / (n * (n - 1))

    '''
    Given an existing graph (from networkx), predict the parameters that should be used given.
    Returns (n,k,p), where:
    n: the number of nodes
    k: the degree of nodes of the starting regular graph (that we rewire)
    p: the probability of rewiring
    '''

    def predict_small_world(self):
        n = len(self.__g.nodes())
        k = sum([len(self.__g.neighbors(i)) for i in self.__g.nodes()]) // (2 * n)
        probs = logspace(-5, 0, 64, False, 10)
        (lvs, cvs, l0, c0) = self.generate_example_graphs(n, k, probs)
        lp = self.average_shortest_path_length()
        l_ratio = lp / l0
        cp = self.average_clustering()
        c_ratio = cp / c0

        # Find the p according to l and c ratios
        index_l = self.closest_index(lvs, l_ratio)
        index_c = self.closest_index(cvs, c_ratio)
        prob_l = probs[index_l]
        prob_c = probs[index_c]

        p = (prob_l + prob_c) / 2
        return n, k, p

    @staticmethod
    def closest_index(values, target):
        min_diff = INFINITY
        best = 0
        for i in range(len(values)):
            lv = values[i]
            diff = abs(lv - target)
            if diff < min_diff:
                best = i
                min_diff = diff
        return best

    '''
    For a set of p-values, generate existing WS graphs and get the values of L(p)/L(0) and C(p)/C(0).
    Returns (l_values, c_values, l0, c0)
    '''

    @staticmethod
    def generate_example_graphs(n, k, ps):
        generator0 = WattsStrogatzGenerator(n, k, 0)
        graph0 = generator0.generate()
        pred0 = ParameterPrediction(graph0)
        l0 = pred0.average_shortest_path_length()
        c0 = pred0.average_clustering()
        result = ([], [], l0, c0)
        for p in ps:
            l_tot = 0
            c_tot = 0
            generator = WattsStrogatzGenerator(n, k, p)
            for i in range(TRIALS):
                graph = generator.generate()
                pred_i = ParameterPrediction(graph)
                l_tot += pred_i.average_shortest_path_length()
                c_tot += pred_i.average_clustering()
            lp = l_tot / TRIALS
            cp = c_tot / TRIALS
            result[0].append(lp / l0)
            result[1].append(cp / c0)
        return result


def test_parameter_prediction():
    print("Testing small world prediction with obviously Watts-Strogatz Graph (50,6,0.1)")
    generator = WattsStrogatzGenerator(50, 6, 0.1)
    pred = ParameterPrediction(generator.generate())
    print(pred.predict_small_world())


if __name__ == '__main__':
    test_parameter_prediction()
