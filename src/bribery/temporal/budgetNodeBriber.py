from bribery.temporal.briber import TemporalBriber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction
import random


class BudgetNodeBriber(TemporalBriber):

    def __init__(self, u0, k=0.1, i=7, b=0.5):
        super().__init__(u0)
        self._k = k
        # TODO @callum: rename variables to better explain their purpose, make package-private where appropriate
        self.c = 0
        self.i = i
        self.pr = 0
        self.npr = 0
        self.pri = 0
        self.nid = 0
        # TODO @callum: how is budget required? Isn't this roughly equivalent to utility (self._u)?
        self.budget = b

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
        if self.c >= self.i:
            next_act.add_bribe(self.nid, min(self._u,
                                             self._g.get_max_rating() - self._g.get_vote(self.nprd))) 
            # TODO @callum: self.nprd not defined in __init__ - did you mean self.npr?
            self.c = 0
            self.pr = self._g.eval_graph(self.get_briber_id())
        else:
            next_node = self._g.get_random_customer()
            next_act.add_bribe(next_node, self._k)
            self.npr = self._g.eval_graph(self.get_briber_id())
            self.c = self.c + 1
            if self.npr - self.pr > self.pri and \
                    min(self._u, (1 - self._g.get_vote(self.nid))) <= self.budget:
                self.nid = next_node
                self.pri = self.npr - self.pr
            self.pr = self.npr
        return next_act
