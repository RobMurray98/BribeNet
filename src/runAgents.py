import matplotlib.pyplot as plt
from bribery.oneMoveRandom import OneMoveRandom
from bribery.oneMoveINB import OneMoveINB
from graphGenerator import RatingGraph


# Returns list of scores over the time of run
# Inputs A and B should be the class of agent used
def run_agents(A, B, init_u=10, moves=20):
    # Two identical graphs
    g1 = RatingGraph()
    g2 = g1.copy()
    # Agents running on identical graphs
    agent_a = A(g1, init_u)
    agent_b = B(g2, init_u)
    # scores over time
    scores_a = [g1.eval_graph()]
    scores_b = [g2.eval_graph()]

    for i in range(0, moves):
        # Bribe A
        agent_a.next_bribe()
        scores_a.append(g1.eval_graph())
        # Bribe B
        agent_b.next_bribe()
        scores_b.append(g2.eval_graph())

    return scores_a, scores_b


# plots two lists of scores on a graph, saved to filename
def plot_scores(scores_a, scores_b, label_a, label_b, filename="graphrun.png"):
    print(scores_a)
    print(scores_b)
    print(label_a)
    print(label_b)
    xs = [i for i in range(0, len(scores_a))]
    plt.plot(xs, scores_a, color="red", label=label_a)
    plt.plot(xs, scores_b, color="orange", label=label_b)
    plt.xlabel("Moves over time")
    plt.ylabel("Average P-rating")
    plt.legend(loc="upper left")
    plt.savefig(filename)
    plt.clf()


def main():
    a, b = run_agents(OneMoveRandom, OneMoveINB)
    plot_scores(a, b, "Random Bribing Agent", "Influential Node Bribing Agent")


if __name__ == '__main__':
    main()
