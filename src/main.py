from bribery.influentialNode import InfluentialNodeBriber
from bribery.mostInfluencialNode import MostInfluentialNodeBriber
from bribery.random import RandomBriber
from graphGenerator import RatingGraph
from parameterPrediction import testParameterPrediction
# from parameterPrediction import predictSmallWorld
# from snapImport import facebook


# briber: function that takes a graph and returns a briber
def graph_and_test(briber_setup, graph):
    print(graph.evalGraph())
    print("Bribing!")
    briber = briber_setup(graph)
    briber.nextBribe()
    print(graph.evalGraph())
    print("")


if __name__ == "__main__":
    print("Testing parameter prediction!")
    testParameterPrediction()
    print("")
    rating_graph = RatingGraph()
    print("Testing random bribery on a graph!")
    graph_and_test(lambda g: RandomBriber(g, 10), rating_graph.copy())
    print("Testing influential node bribery on a graph!")
    graph_and_test(lambda g: InfluentialNodeBriber(g, 10, 0.2), rating_graph.copy())
    print("Testing most influential node bribery on a graph!")
    graph_and_test(lambda g: MostInfluentialNodeBriber(g, 10, 0.2), rating_graph.copy())
