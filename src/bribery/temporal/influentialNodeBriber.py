from bribery.temporal.briber import TemporalBriber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction
import random


class InfluentialNodeBriber(TemporalBriber):

    def __init__(self, u0, k=0.1):
        super().__init__(u0)
        self._k = k
        # TODO @callum: rename variables to better explain their purpose, make package-private where appropriate
        self.pr = 0
        self.npr = 0
        self.nprd = 0

    def _set_graph(self, g):
        super()._set_graph(g)
        # Make sure that k is set such that there are enough resources left to actually bribe people.
        self._k = min(self._k, 0.5 * (self._u / self._g.customer_count()))
        self.pr = self._g.eval_graph(self.get_briber_id())
        self.npr = self.pr

    def next_action(self) -> SingleBriberyAction:
        # TODO @callum: docstring to describe nature of action returned
        # TODO @callum: implement tests for correct function
        next_act = SingleBriberyAction(self)
        if self.npr > self.pr:
            next_act.add_bribe(self.nprd, min(self.get_resources(),
                                              self._g.get_max_rating() - self._g.get_vote(self.nprd)))
            self.pr = self.npr
        else:
            next_node = self._g.get_random_customer()
            next_act.add_bribe(next_node, self._k)
            self.npr = self._g.eval_graph(self.get_briber_id())
            self.nprd = next_node
        return next_act
