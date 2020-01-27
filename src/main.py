from copy import deepcopy

from bribery.static.influentialNodeBriber import InfluentialNodeBriber
from bribery.static.mostInfluencialNodeBriber import MostInfluentialNodeBriber
from bribery.static.randomBriber import RandomBriber
from graph.static.ratingGraph import StaticRatingGraph
from prediction.parameterPrediction import test_parameter_prediction


# from snapImport import facebook


# briber: function that takes a graph and returns a briber
def graph_and_test(graph):
    # noinspection PyProtectedMember
    print(graph.eval_graph())
    print("Bribing!")
    # noinspection PyProtectedMember
    graph._bribers[0].next_bribe()
    print(graph.eval_graph())
    print("")


if __name__ == "__main__":
    print("Testing parameter prediction!")
    test_parameter_prediction()
    print("")
    bribers = (RandomBriber(10), InfluentialNodeBriber(10, k=0.2), MostInfluentialNodeBriber(10, k=0.2))
    print("Testing random bribery on a graph!")
    graph_and_test(StaticRatingGraph(tuple([bribers[0]])))
    print("Testing influential node bribery on a graph!")
    graph_and_test(StaticRatingGraph(tuple([bribers[1]])))
    print("Testing most influential node bribery on a graph!")
    graph_and_test(StaticRatingGraph(tuple([bribers[2]])))
