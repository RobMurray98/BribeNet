import enum
from typing import List

from bribery.briber import Briber
from bribery.influentialNodeBriber import InfluentialNodeBriber
from bribery.mostInfluencialNodeBriber import MostInfluentialNodeBriber
from bribery.nonBriber import NonBriber
from bribery.oneMoveInfluentialNodeBriber import OneMoveInfluentialNodeBriber
from bribery.oneMoveRandomBriber import OneMoveRandomBriber
from bribery.randomBriber import RandomBriber
from graph.multiBriberRatingGraph import MultiBriberRatingGraph
from graph.ratingGraph import RatingGraph, DEFAULT_GEN
from graph.singleBriberRatingGraph import SingleBriberRatingGraph


@enum.unique
class BriberID(enum.Enum):
    Non = 0
    Random = 1
    OneMoveRandom = 2
    InfluentialNode = 3
    MostInfluentialNode = 4
    OneMoveInfluentialNode = 5

    @classmethod
    def get_briber_constructor(cls, idx):
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
        return lambda u0, args, kwargs: c(u0, *args, **kwargs)


class RatingGraphBuilder(object):

    def __init__(self):
        self.bribers: List[Briber] = []
        self.generator = DEFAULT_GEN

    def add_builder(self, briber: BriberID, u0: int = 0, *args, **kwargs):
        self.bribers.append(BriberID.get_briber_constructor(briber)(u0, *args, **kwargs))

    def set_generator(self, generator):
        self.generator = generator

    def build(self) -> RatingGraph:
        if not self.bribers:
            return SingleBriberRatingGraph(None)
        if len(self.bribers) == 1:
            rg = SingleBriberRatingGraph(self.bribers[0])
        else:
            rg = MultiBriberRatingGraph(tuple(self.bribers))
        return rg
