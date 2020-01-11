from bribery.influentialNodeBriber import InfluentialNodeBriber
from graphGenerator import RatingGraph


def main():
    g = RatingGraph()
    inb = InfluentialNodeBriber(g, 100.0)
    print(inb.__u)
    for _ in range(20):
        inb.next_bribe()
        print(inb.__u)


if __name__ == '__main__':
    main()
