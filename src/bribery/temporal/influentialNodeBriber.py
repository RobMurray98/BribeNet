from bribery.temporal.briber import TemporalBriber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction
import random


class InfluentialNodeBriber(TemporalBriber):
    # TODO: implement influential node behaviour that returns multiBriberyAction

    def __init__(self, u0, k=0.1):
        super().__init__(u0)
        self.k = k  # will be reassigned when graph
        self.pr = 0
        self.npr = 0
        self.nprd = 0

    def _set_graph(self, g):
        super()._set_graph(g)
        # Make sure that k is set such that there are enough resources left to actually bribe people.
        self.k = min(self.k, 0.5 * (self._u / self._g.customer_count()))
        self.pr = self.get_graph().eval_graph(self.get_briber_id())
        self.npr = self.pr

    def next_action(self) -> SingleBriberyAction:
        nextAct = SingleBriberyAction(self)
        if self.npr > self.pr:
            nextAct.add_bribe(self.nprd, min(self.get_resources(),
                                             self._g.get_max_rating() - self._g.get_vote(self.nprd)))
            self.pr = self.npr
        else:
            nNode = self.get_graph().get_random_customer()
            nextAct.add_bribe(nNode, self.k)
            self.npr = self.get_graph().eval_graph(self.get_briber_id())
            self.nprd = nNode
        return nextAct
