import enum
import sys
from typing import List

from BribeNet.bribery.briber import Briber
from BribeNet.bribery.static.influentialNodeBriber import InfluentialNodeBriber
from BribeNet.bribery.static.mostInfluentialNodeBriber import MostInfluentialNodeBriber
from BribeNet.bribery.static.nonBriber import NonBriber
from BribeNet.bribery.static.oneMoveInfluentialNodeBriber import OneMoveInfluentialNodeBriber
from BribeNet.bribery.static.oneMoveRandomBriber import OneMoveRandomBriber
from BribeNet.bribery.static.randomBriber import RandomBriber
from BribeNet.graph.ratingGraph import DEFAULT_GEN
from BribeNet.graph.static.ratingGraph import StaticRatingGraph


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
        self.bribers.append(BriberType.get_briber_constructor(briber, *args, **kwargs)(u0))
        return self

    def set_generator(self, generator):
        self.generator = generator
        return self

    def build(self) -> StaticRatingGraph:
        if not self.bribers:
            print("WARNING: StaticRatingGraph built with no bribers. Using NonBriber...", file=sys.stderr)
            return StaticRatingGraph(tuple([NonBriber(0)]))
        return StaticRatingGraph(tuple(self.bribers))
