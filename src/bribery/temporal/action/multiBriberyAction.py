import sys
from typing import Dict, Optional, List

from bribery.temporal.action.briberyAction import BriberyAction
from bribery.temporal.action.singleBriberyAction import SingleBriberyAction


class MultiBriberyAction(BriberyAction):

    def __init__(self, graph, bribes: Optional[Dict[int, Dict[int, float]]] = None):
        from graph.temporal.ratingGraph import TemporalRatingGraph
        assert issubclass(graph.__class__, TemporalRatingGraph)
        super().__init__(graph=graph)
        if bribes is not None:
            for _, bribe in bribes.items():
                for _, value in bribe.items():
                    assert value > 0, "bribe quantity must be greater than 0"
        self.bribes: Dict[int, Dict[int, float]] = bribes or {}

    @classmethod
    def make_multi_action_from_single_actions(cls, actions: List[SingleBriberyAction]):
        assert len(actions) > 0, "must be at least one bribery action"
        graph = actions[0].briber.get_graph()
        assert all(b.briber.get_graph() is graph for b in actions), "all actions must be on same graph"
        time_step = actions[0].get_time_step()
        assert all(b.get_time_step() == time_step for b in actions), "all actions must be at same time"
        return cls(graph=graph, bribes={b.briber.get_briber_id(): b.bribes for b in actions})

    def add_bribe(self, briber_id: int, node_id: int, bribe: float):
        assert bribe > 0, "bribe quantity must be greater than 0"
        assert node_id in self.graph.get_customers(), "node not present in graph"
        assert briber_id in range(len(self.graph.get_bribers())), "briber not present"
        if briber_id in self.bribes:
            if node_id in self.bribes[briber_id]:
                print("WARNING: node bribed twice in single time step, combining...", file=sys.stderr)
                self.bribes[briber_id][node_id] += bribe
            else:
                self.bribes[briber_id][node_id] = bribe
        else:
            self.bribes[briber_id] = {node_id: bribe}

    def _perform_action(self):
        bribers = self.graph.get_bribers()
        for briber_id, bribe in self.bribes.items():
            assert sum(bribe.values()) <= bribers[briber_id].get_resources(), \
                f"MultiBriberyAction exceeded resources available to briber {briber_id}: {str(bribers[briber_id])}"
        for briber_id, bribe in self.bribes.items():
            for customer, value in bribe.items():
                bribers[briber_id].bribe(node_id=customer, amount=value)

    def is_bribed(self, node_id):
        bribers = []
        for briber_id in self.bribes:
            if node_id in self.bribes[briber_id]:
                bribers.append(briber_id)
        if not bribers:
            return False, bribers
        return True, bribers
