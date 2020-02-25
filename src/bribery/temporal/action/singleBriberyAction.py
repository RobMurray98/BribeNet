import sys
from typing import Dict, Optional

from bribery.temporal.action.briberyAction import BriberyAction
from bribery.temporal.action import BribeMustBeGreaterThanZeroException, NodeDoesNotExistException,\
    BriberyActionExceedsAvailableUtilityException


class SingleBriberyAction(BriberyAction):

    def __init__(self, briber, bribes: Optional[Dict[int, float]] = None):
        from bribery.temporal.briber import TemporalBriber
        assert issubclass(briber.__class__, TemporalBriber)
        super().__init__(graph=briber.get_graph())
        if bribes is not None:
            for _, bribe in bribes.items():
                if bribe <= 0:
                    raise BribeMustBeGreaterThanZeroException()
        self.briber = briber
        self._bribes: Dict[int, float] = bribes or {}
        self.__time = self.briber.get_graph().get_time_step()

    def add_bribe(self, node_id: int, bribe: float):
        if bribe <= 0:
            raise BribeMustBeGreaterThanZeroException()
        if node_id not in self.briber.get_graph().get_customers():
            raise NodeDoesNotExistException()
        if node_id in self._bribes:
            print(f"WARNING: node {node_id} bribed twice in single time step, combining...", file=sys.stderr)
            self._bribes[node_id] += bribe
        else:
            self._bribes[node_id] = bribe

    def _perform_action(self):
        if sum(self._bribes.values()) > self.briber.get_resources():
            raise BriberyActionExceedsAvailableUtilityException()
        for customer, bribe in self._bribes.items():
            self.briber.bribe(node_id=customer, amount=bribe)

    def is_bribed(self, node_id):
        if node_id in self._bribes:
            return True, [self.briber.get_briber_id()]
        return False, []
