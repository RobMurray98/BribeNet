from bribery.temporal.briber import TemporalBriber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction
import random


class MostInfluentialNodeBriber(TemporalBriber):

    def __init__(self, u0: float, k: float = 0.1, i: int = 7):
        """
        Constructor
        :param u0: initial utility
        :param k: cost if information
        :param i: maximum loop iterations for finding most influential node
        """
        super().__init__(u0)
        self._k = k
        self._c = 0  # current loop iteration
        self._i = i  # maximum loop iterations for finding most influential node
        self._current_rating = 0
        self._previous_rating = 0
        self._max_rating_increase = 0
        self._best_node = 0
        self._next_node = 0
        self._last_node = 0

    def _set_graph(self, g):
        super()._set_graph(g)
        # Make sure that k is set such that there are enough resources left to actually bribe people.
        self._k = min(self._k, 0.5 * (self._u / self._g.customer_count()))
        self._current_rating = self._g.eval_graph(self.get_briber_id())
        self._previous_rating = self._current_rating
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
        self._current_rating = self._g.eval_graph(self.get_briber_id())
        next_act = SingleBriberyAction(self)
        self._next_node = self._g.get_random_customer()
        if self._current_rating - self._previous_rating > self._max_rating_increase:
            self._best_node = self._last_node
            self._max_rating_increase = self._current_rating - self._previous_rating
        if self._c >= self._i:
            next_act.add_bribe(self._best_node, min(self.get_resources(),
                                                    self._g.get_max_rating() - self._g.get_vote(self._best_node)))
            self._c = 0
        else:
            next_act.add_bribe(self._next_node, self._k)
            self._c = self._c + 1
        self._last_node = self._next_node
        self._previous_rating = self._current_rating
        return next_act
