from graphGenerator import ratingGraph
from staticBribingAgent import randomBriber, influentialNodeBriber, mostInfluentialNodeBriber
from parameterPrediction import predictSmallWorld, testParameterPrediction
from snapImport import facebook

# briber: function that takes a graph and returns a briber
def graphAndTest(briberSetup, graph):
    print(graph.evalGraph())
    print("Bribing!")
    briber = briberSetup(graph)
    briber.nextBribe()
    print(graph.evalGraph())
    print("")

if __name__ == "__main__":
    print("Testing parameter prediction!")
    testParameterPrediction()
    print("")
    graph = ratingGraph()
    print("Testing random bribery on a graph!")
    graphAndTest(lambda g: randomBriber(g, 10), graph.copy())
    print("Testing influential node bribery on a graph!")
    graphAndTest(lambda g: influentialNodeBriber(g, 10, 0.2), graph.copy())
    print("Testing most influential node bribery on a graph!")
    graphAndTest(lambda g: mostInfluentialNodeBriber(g, 10, 0.2), graph.copy())
