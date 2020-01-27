import enum
import sys
from typing import List

from bribery.briber import Briber
from bribery.static.influentialNodeBriber import InfluentialNodeBriber
from bribery.static.mostInfluencialNodeBriber import MostInfluentialNodeBriber
from bribery.static.nonBriber import NonBriber
from bribery.static.oneMoveInfluentialNodeBriber import OneMoveInfluentialNodeBriber
from bribery.static.oneMoveRandomBriber import OneMoveRandomBriber
from bribery.static.randomBriber import RandomBriber
from graph.static.ratingGraph import StaticRatingGraph
from graph.ratingGraph import RatingGraph, DEFAULT_GEN
from test.bribery.static.briberTestCase import DummyBriber


@enum.unique
class BriberType(enum.Enum):
    Non = 0
    Random = 1
    OneMoveRandom = 2
    InfluentialNode = 3
    MostInfluentialNode = 4
    OneMoveInfluentialNode = 5

    @classmethod
    def get_briber_constructor(cls, idx, *args, **kwargs):
        c = None
        if idx == cls.Non:
            c = NonBriber
        if idx == cls.Random:
            c = RandomBriber
        if idx == cls.OneMoveRandom:
            c = OneMoveRandomBriber
        if idx == cls.InfluentialNode:
            c = InfluentialNodeBriber
        if idx == cls.MostInfluentialNode:
            c = MostInfluentialNodeBriber
        if idx == cls.OneMoveInfluentialNode:
            c = OneMoveInfluentialNodeBriber
        return lambda u0: c(u0, *args, **kwargs)


class RatingGraphBuilder(object):

    def __init__(self):
        self.bribers: List[Briber] = []
        self.generator = DEFAULT_GEN

    def add_briber(self, briber: BriberType, u0: int = 0, *args, **kwargs):
        self.bribers.append(BriberType.get_briber_constructor(briber)(u0, *args, **kwargs))
        return self

    def set_generator(self, generator):
        self.generator = generator
        return self

    def build(self) -> StaticRatingGraph:
        if not self.bribers:
            print("WARNING: StaticRatingGraph built with no bribers. Using DummyBriber...", file=sys.stderr)
            return StaticRatingGraph(tuple([DummyBriber(0)]))
        return StaticRatingGraph(tuple(self.bribers))
