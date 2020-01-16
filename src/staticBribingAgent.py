from bribery.static.influentialNodeBriber import InfluentialNodeBriber
from graph.static.singleBriberRatingGraph import SingleBriberRatingGraph


def main():
    inb = InfluentialNodeBriber(100.0)
    g = SingleBriberRatingGraph(inb)
    inb._set_graph(g)
    print(inb.get_resources())
    for _ in range(20):
        inb.next_bribe()
        print(inb.get_resources())


if __name__ == '__main__':
    main()
