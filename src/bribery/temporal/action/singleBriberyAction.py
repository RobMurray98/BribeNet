import sys
from typing import Dict, Optional

from bribery.temporal.action.briberyAction import BriberyAction


class SingleBriberyAction(BriberyAction):

    def __init__(self, briber, bribes: Optional[Dict[int, float]] = None):
        from bribery.temporal.briber import TemporalBriber
        assert issubclass(briber.__class__, TemporalBriber)
        super().__init__(graph=briber.get_graph())
        if bribes is not None:
            for _, bribe in bribes.items():
                assert bribe > 0, "bribe quantity must be greater than 0"
        self.briber = briber
        self.bribes: Dict[int, float] = bribes or {}
        self.__time = self.briber.get_graph().get_time_step()

    def add_bribe(self, node_id: int, bribe: float):
        assert bribe > 0, "bribe quantity must be greater than 0"
        if node_id in self.bribes.keys():
            print(f"WARNING: node {node_id} bribed twice in single time step, combining...", file=sys.stderr)
            self.bribes[node_id] += bribe
        else:
            self.bribes[node_id] = bribe

    def _perform_action(self):
        assert sum(self.bribes.values()) <= self.briber.get_resources(), "SingleBriberyAction exceeded resources " \
                                                                         "available to briber"
        for customer, bribe in self.bribes.items():
            self.briber.bribe(node_id=customer, amount=bribe)
