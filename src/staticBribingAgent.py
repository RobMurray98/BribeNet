from bribery.influentialNode import InfluentialNodeBriber
from graphGenerator import RatingGraph


def main():
    g = RatingGraph()
    inb = InfluentialNodeBriber(g, 100.0)
    print(inb.u)
    for _ in range(20):
        inb.next_bribe()
        print(inb.u)


if __name__ == '__main__':
    main()
