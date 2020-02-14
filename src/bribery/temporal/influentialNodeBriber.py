from bribery.temporal.briber import TemporalBriber
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction
import random


class InfluentialNodeBriber(TemporalBriber):

    def __init__(self, u0: float, k: float = 0.1):
        """
        Constructor
        :param u0: initial utility
        :param k: cost of information
        """
        super().__init__(u0)
        self._k = k
        self._current_rating = 0
        self._previous_rating = 0
        self._next_node = 0

    def _set_graph(self, g):
        super()._set_graph(g)
        # Make sure that k is set such that there are enough resources left to actually bribe people.
        self._k = min(self._k, 0.5 * (self._u / self._g.customer_count()))
        self._current_rating = self._g.eval_graph(self.get_briber_id())
        self._previous_rating = self._current_rating

    def next_action(self) -> SingleBriberyAction:
        """ Returns next action of briber

        Returns: SingleBriberyAction for the briber to take in the next temporal time step

        """
        # TODO @callum: docstring to describe nature of action returned
        # TODO @callum: implement tests for correct function
        self._current_rating = self._g.eval_graph(self.get_briber_id())
        next_act = SingleBriberyAction(self)
        if self._current_rating > self._previous_rating:
            next_act.add_bribe(self._next_node, min(self.get_resources(),
                                                    self._g.get_max_rating() - self._g.get_vote(self._next_node)))
        else:
            self._next_node = self._g.get_random_customer()
            next_act.add_bribe(self._next_node, self._k)
        self._previous_rating = self._current_rating
        return next_act
