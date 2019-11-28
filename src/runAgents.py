import matplotlib.pyplot as plt
from bribery.oneMoveRandom import OneMoveRandom
from bribery.oneMoveINB import OneMoveINB
from graphGenerator import RatingGraph
from numpy import cumsum

# Returns list of scores over the time of run
# Inputs A and B should be the class of agent used
def run_agents(A, B, init_u=10, moves=20):
    # Two identical graphs
    g1 = RatingGraph()
    g2 = g1.copy()
    # Agents running on identical graphs
    agentA = A(g1, init_u)
    agentB = B(g2, init_u)
    # scores over time
    scoresA = [g1.eval_graph()]
    scoresB = [g2.eval_graph()]

    for i in range(0, moves):
        # Bribe A
        agentA.next_bribe()
        scoresA.append(g1.eval_graph())
        # Bribe B
        agentB.next_bribe()
        scoresB.append(g2.eval_graph())

    return scoresA, scoresB, agentA.get_spent(), agentB.get_spent()

# plots two lists of scores on a graph, saved to filename
def plot_scores(scoresA, scoresB, labelA, labelB, filename="graphrun.png"):

    xs = [i for i in range(0, len(scoresA))]
    plt.plot(xs, scoresA, color="red", label=labelA)
    plt.plot(xs, scoresB, color="orange", label=labelB)
    plt.xlabel("Moves over time")
    plt.ylabel("Average P-rating")
    plt.legend(loc="upper left")
    plt.savefig(filename)
    plt.clf()

def plot_cost(scoresA, scoresB, costA, costB, labelA, labelB, filename="costrun.png"):

    plt.plot(costA, scoresB, color="red", label=labelA)
    plt.plot(costB, scoresB, color="orange", label=labelB)
    plt.xlabel("Amount spent")
    plt.ylabel("Average P-rating")
    plt.legend(loc="upper left")
    plt.savefig(filename)
    plt.clf()

def main():
    A, B, sA, sB = run_agents(OneMoveRandom, OneMoveINB)
    print(sA)
    print(sB)
    sA = cumsum(sA)
    sB = cumsum(sB)
    plot_scores(A, B, "Random Bribing Agent", "Influential Node Bribing Agent")
    plot_cost(A, B, sA, sB, "Random Bribing Agent", "Influential Node Bribing Agent")

if __name__ == '__main__':
    main()
