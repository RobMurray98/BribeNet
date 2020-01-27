import sys
from typing import Dict, Optional


class BriberyAction(object):

    def __init__(self, bribes: Optional[Dict[int, float]] = None):
        if bribes is not None:
            for _, bribe in bribes:
                assert bribe > 0, "bribe quantity must be greater than 0"
        self.bribes: Dict[int, float] = bribes or {}

    def add_bribe(self, node_id: int, bribe: float):
        assert bribe > 0, "bribe quantity must be greater than 0"
        if node_id in self.bribes.keys():
            print("WARNING: node bribed twice in single time step, combining...", file=sys.stderr)
            self.bribes[node_id] += bribe
        else:
            self.bribes[node_id] = bribe
