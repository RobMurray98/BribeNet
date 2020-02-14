from bribery.temporal.briber import TemporalBriber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction
import random


class BudgetNodeBriber(TemporalBriber):

    def __init__(self, u0, k=0.1, b=0.5):
        super().__init__(u0)
        self._k = k
        # TODO @callum: rename variables to better explain their purpose, make package-private where appropriate
        # _cpr is current p_rating
        # _ppr is past p_rating
        # _nid is next good node found
        # _budget defines how much they are willing to spend on any single bribe
        self._cpr = 0
        self._ppr = 0
        self._nid = 0
        # TODO @callum: how is budget required? Isn't this roughly equivalent to utility (self._u)?
        self._budget = b

    def _set_graph(self, g):
        super()._set_graph(g)
        # Make sure that k is set such that there are enough resources left to actually bribe people.
        self._k = min(self._k, 0.5 * (self._u / self._g.customer_count()))
        self._cpr = self._g.eval_graph(self.get_briber_id())
        self._ppr = self._cpr

    def next_action(self) -> SingleBriberyAction:
        """ Returns next action of briber

        Returns: SingleBriberyAction for the briber to take in the next temporal time step

        """
        # TODO @callum: docstring to describe nature of action returned 
        # TODO @callum: implement tests for correct function
        self._cpr = self._g.eval_graph(self.get_briber_id())
        next_act = SingleBriberyAction(self)
        if self._cpr > self._ppr and \
                    min(self._u, (1 - self._g.get_vote(self._nid))) <= self._budget:
            next_act.add_bribe(self._nid, min(self.get_resources(),
                                              self._g.get_max_rating() - self._g.get_vote(self._nid)))
        else:
            self._nid = self._g.get_random_customer()
            next_act.add_bribe(self._nid, self._k)
        self._ppr = self._cpr
        return next_act
