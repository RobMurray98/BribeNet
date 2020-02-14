from bribery.temporal.briber import TemporalBriber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction
import random


class MostInfluentialNodeBriber(TemporalBriber):

    # TODO: implement influential node behaviour that returns multiBriberyAction
    def __init__(self, u0, k=0.1, i=7):
        super().__init__(u0)
        self._k = k
        # TODO @callum: rename variables to better explain their purpose, make package-private where appropriate
        # _cpr is current p_rating
        # _ppr is past p_rating
        # _nnode is next node to test
        # _nid is best node found so far
        # _c is for tracking current loop iteration
        # _i defines max loop iterations
        # _pri tracks maximum observed p-rating increase to find most influential node
        # _lnode tracks last observed node
        self._c = 0
        self._i = i
        self._cpr = 0
        self._ppr = 0
        self._pri = 0
        self._nid = 0
        self._nnode = 0
        self._lnode = 0

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
        # TODO @callum: a lot of repeated code between influential temporal bribers,
        #               factor out (class or function level)
        self._cpr = self._g.eval_graph(self.get_briber_id())
        next_act = SingleBriberyAction(self)
        self._nnode = self._g.get_random_customer()
        if self._cpr - self._ppr > self._pri:
            self._nid = self._lnode
            self._pri = self._cpr - self._ppr
        if self.c >= self.i:
            next_act.add_bribe(self._nid, min(self.get_resources(),
                                             self._g.get_max_rating() - self._g.get_vote(self._nid)))
            self._c = 0
        else:
            next_act.add_bribe(self._nnode, self._k)
            self._c = self._c + 1
        self._lnode = self._nnode
        self._ppr = self._cpr
        return next_act
