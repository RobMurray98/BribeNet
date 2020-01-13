from copy import deepcopy

from bribery.influentialNodeBriber import InfluentialNodeBriber
from bribery.mostInfluencialNodeBriber import MostInfluentialNodeBriber
from bribery.randomBriber import RandomBriber
from graph.ratingGraph import RatingGraph
from parameterPrediction import test_parameter_prediction
# from snapImport import facebook


# briber: function that takes a graph and returns a briber
def graph_and_test(briber_setup, graph):
    print(graph.eval_graph())
    print("Bribing!")
    briber = briber_setup(graph)
    briber.next_bribe()
    print(graph.eval_graph())
    print("")


if __name__ == "__main__":
    print("Testing parameter prediction!")
    test_parameter_prediction()
    print("")
    rating_graph = RatingGraph()
    print("Testing random bribery on a graph!")
    graph_and_test(lambda g: RandomBriber(g, 10), deepcopy(rating_graph))
    print("Testing influential node bribery on a graph!")
    graph_and_test(lambda g: InfluentialNodeBriber(g, 10, 0.2), deepcopy(rating_graph))
    print("Testing most influential node bribery on a graph!")
    graph_and_test(lambda g: MostInfluentialNodeBriber(g, 10, 0.2), deepcopy(rating_graph))
