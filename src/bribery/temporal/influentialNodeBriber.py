from bribery.temporal.briber import TemporalBriber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from random import random


class InfluentialNodeBriber(TemporalBriber):
    # TODO: implement influential node behaviour that returns BriberyAction

    def __init__(self, u0, k=0.1, i=7):
        super().__init__(u0)
        self.k = k  # will be reassigned when graph
        self.c = 0
        self.i = i
        self.pr = 0
        self.npr = 0
        self.nprd = 0

    @override
    def _set_graph(self, g):
        super()._set_graph(g)
        # Make sure that k is set such that there are enough resources left to actually bribe people.
        self.k = min(self.k, 0.5 * (self._u / self._g.customer_count()))
        self.pr = self.get_graph.eval_graph(self.get_briber_id)
        self.npr = self.pr

    def next_action(self) -> SingleBriberyAction:
        nextAct = SingleBriberyAction(self)
        if self.npr>self.pr:
            nextAct.add_bribe(self.nprd, min(self.get_resources, (1-self.get_graph.getvote(self.nprd))))
            self.pr = self.npr
        else:
            mNode = len(self.get_graph.nodes)
            nNode = random.randInt(mNode)
            nextAct.add_bribe(nNode, self.k)
            self.npr = self.get_graph.eval_graph(self.get_briber_id)
            self.nprd = nNode
        return nextAct
