import sys

from BribeNet.bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from BribeNet.bribery.temporal.briber import TemporalBriber


class BudgetNodeBriber(TemporalBriber):

    def __init__(self, u0: float, k: float = 0.1, b: float = 0.5):
        """
        Constructor
        :param u0: initial utility
        :param k: cost of information
        :param b: budget, a maximum they are willing to spend on any single bribe
        """
        super().__init__(u0)
        self._k = k
        self._current_rating = None
        self._previous_rating = None
        self._next_node = 0
        self._budget = b
        self._info_gained = set()
        self._bribed = set()

    def _set_graph(self, g):
        super()._set_graph(g)
        # Make sure that k is set such that there are enough resources left to actually bribe people.
        self._k = min(self._k, 0.5 * (self.get_resources() / self.get_graph().customer_count()))

    def _next_action(self) -> SingleBriberyAction:
        """
        Next action of briber, either to gain information or to fully bribe an influential node
        :return: SingleBriberyAction for the briber to take in the next temporal time step
        """
        self._current_rating = self.get_graph().eval_graph(self.get_briber_id())
        if self._previous_rating is None:
            self._previous_rating = self._current_rating
        next_act = SingleBriberyAction(self)
        maximum_bribe = (self.get_graph().get_max_rating()
                         - self.get_graph().get_vote(self._next_node)[self.get_briber_id()])
        if self._current_rating > self._previous_rating and min(self.get_resources(), maximum_bribe) <= self._budget \
                and self._next_node not in self._bribed and maximum_bribe > 0:
            next_act.add_bribe(self._next_node, min(self.get_resources(), maximum_bribe))
            self._bribed.add(self._next_node)
            self._info_gained = set()
        else:
            try:
                self._next_node = self._g.get_random_customer(excluding=self._info_gained | self._bribed)
            except IndexError:
                print(f"WARNING: {self.__class__.__name__} found no influential nodes, not acting...", file=sys.stderr)
                return next_act
            next_act.add_bribe(self._next_node, min(maximum_bribe, min(self.get_resources(), self._k)))
            self._info_gained.add(self._next_node)
        self._previous_rating = self._current_rating
        return next_act
