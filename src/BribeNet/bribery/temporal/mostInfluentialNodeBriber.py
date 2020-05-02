import sys

from BribeNet.bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from BribeNet.bribery.temporal.briber import TemporalBriber


class MostInfluentialNodeBriber(TemporalBriber):

    def __init__(self, u0: float, k: float = 0.1, i: int = 7):
        """
        Constructor
        :param u0: initial utility
        :param k: cost of information
        :param i: maximum loop iterations for finding most influential node
        """
        super().__init__(u0)
        self._k = k
        self._c = 0  # current loop iteration
        self._i = i  # maximum loop iterations for finding most influential node
        self._current_rating = 0
        self._previous_rating = 0
        self._max_rating_increase = 0
        self._best_node = None
        self._next_node = 0
        self._last_node = 0
        self._info_gained = set()
        self._bribed = set()

    def _set_graph(self, g):
        super()._set_graph(g)
        # Make sure that k is set such that there are enough resources left to actually bribe people.
        self._k = min(self._k, 0.5 * (self.get_resources() / self.get_graph().customer_count()))
        self._current_rating = self.get_graph().eval_graph(self.get_briber_id())
        self._previous_rating = self._current_rating

    def _next_action(self) -> SingleBriberyAction:
        """
        Next action of briber, either to gain information or to fully bribe the most influential node
        :return: SingleBriberyAction for the briber to take in the next temporal time step
        """
        self._current_rating = self.get_graph().eval_graph(self.get_briber_id())
        next_act = SingleBriberyAction(self)
        try:
            self._next_node = self.get_graph().get_random_customer(excluding=self._info_gained | self._bribed)
        except IndexError:
            print(f"WARNING: {self.__class__.__name__} found no influential nodes, not acting...", file=sys.stderr)
            return next_act
        if self._current_rating - self._previous_rating > self._max_rating_increase:
            self._best_node = self._last_node
            self._max_rating_increase = self._current_rating - self._previous_rating
        if self._c >= self._i and self._best_node is not None:
            next_act.add_bribe(self._best_node, min(self.get_resources(),
                                                    self.get_graph().get_max_rating()
                                                    - self.get_graph().get_vote(self._best_node)[self.get_briber_id()]))
            self._bribed.add(self._best_node)
            self._info_gained = set()
            self._c = 0
            self._max_rating_increase = 0
            self._best_node = 0
        else:
            if self._c >= self._i:
                print(f"WARNING: {self.__class__.__name__} has not found an influential node in {self._c} tries "
                      f"(intended maximum tries {self._i}), continuing search...",
                      file=sys.stderr)
            next_act.add_bribe(self._next_node, min(self.get_resources(), self._k))
            self._info_gained.add(self._next_node)
            self._c = self._c + 1
        self._last_node = self._next_node
        self._previous_rating = self._current_rating
        return next_act