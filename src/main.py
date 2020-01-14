from copy import deepcopy

from bribery.influentialNodeBriber import InfluentialNodeBriber
from bribery.mostInfluencialNodeBriber import MostInfluentialNodeBriber
from bribery.randomBriber import RandomBriber
from graph.singleBriberRatingGraph import SingleBriberRatingGraph
from parameterPrediction import test_parameter_prediction


# from snapImport import facebook


# briber: function that takes a graph and returns a briber
def graph_and_test(briber, graph):
    briber._set_graph(graph)
    graph._bribers = briber
    print(graph.eval_graph())
    print("Bribing!")
    briber.next_bribe()
    print(graph.eval_graph())
    print("")


if __name__ == "__main__":
    print("Testing parameter prediction!")
    test_parameter_prediction()
    print("")
    bribers = (RandomBriber(10), InfluentialNodeBriber(10, k=0.2), MostInfluentialNodeBriber(10, k=0.2))
    # noinspection PyTypeChecker
    rating_graph = SingleBriberRatingGraph(None)
    print("Testing random bribery on a graph!")
    graph_and_test(bribers[0], deepcopy(rating_graph))
    print("Testing influential node bribery on a graph!")
    graph_and_test(bribers[1], deepcopy(rating_graph))
    print("Testing most influential node bribery on a graph!")
    graph_and_test(bribers[2], deepcopy(rating_graph))
