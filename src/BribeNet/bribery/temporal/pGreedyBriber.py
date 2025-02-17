import sys
import numpy as np

from BribeNet.bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from BribeNet.bribery.temporal.briber import TemporalBriber

"""
IMPORTANT!
This briber cheats and uses the direct influential node information.
This is for testing whether trust is powerful enough to beat P-greedy bribery
even when the briber has perfect information.
"""


class PGreedyBriber(TemporalBriber):

    def __init__(self, u0: float):
        """
        Constructor
        :param u0: initial utility
        """
        super().__init__(u0)
        self._targets = []
        self._index = 0
        self._bribed = set()

    def _set_graph(self, g):
        super()._set_graph(g)
    
    def _get_influential_nodes(self, g):
        # noinspection PyProtectedMember
        influence_weights = [(n, g._get_influence_weight(n, self.get_briber_id())) for n in self._g.get_customers()]
        influence_weights = sorted(influence_weights, key=lambda x: x[1], reverse=True)
        self._targets = [n for (n, w) in influence_weights if w >= 1 and not n in self._bribed]

    def _next_action(self) -> SingleBriberyAction:
        """
        Next action of briber, just bribe the next node as fully as you can.
        :return: SingleBriberyAction for the briber to take in the next temporal time step
        """
        next_act = SingleBriberyAction(self)
        if self._index >= len(self._targets):
            self._get_influential_nodes(self._g)
            self._index = 0
        if self._index < len(self._targets):
            # Bribe the next target as fully as you can.
            target = self._targets[self._index]
            target_vote = self._g.get_vote(target)[self.get_briber_id()]
            if np.isnan(target_vote): target_vote = 0
            next_act.add_bribe(target, min(self.get_resources(),
                                           self._g.get_max_rating() - target_vote))
            self._index += 1
            self._bribed.add(target)
        else:
            print(f"WARNING: {self.__class__.__name__} found no influential nodes, not acting...", file=sys.stderr)
        return next_act
