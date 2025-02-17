import sys
from typing import Dict, Optional, List

from BribeNet.bribery.temporal.action import BribeMustBeGreaterThanZeroException, NodeDoesNotExistException, \
    BriberDoesNotExistException, BriberyActionExceedsAvailableUtilityException
from BribeNet.bribery.temporal.action.briberyAction import BriberyAction
from BribeNet.bribery.temporal.action.singleBriberyAction import SingleBriberyAction
from BribeNet.bribery.temporal.briber import GraphNotSubclassOfTemporalRatingGraphException
from BribeNet.helpers.bribeNetException import BribeNetException


class NoActionsToFormMultiActionException(BribeNetException):
    pass


class BriberyActionsOnDifferentGraphsException(BribeNetException):
    pass


class BriberyActionsAtDifferentTimesException(BribeNetException):
    pass


class MultiBriberyAction(BriberyAction):

    def __init__(self, graph, bribes: Optional[Dict[int, Dict[int, float]]] = None):
        from BribeNet.graph.temporal.ratingGraph import TemporalRatingGraph
        if not issubclass(graph.__class__, TemporalRatingGraph):
            raise GraphNotSubclassOfTemporalRatingGraphException(f"{graph.__class__.__name__} is not a subclass of "
                                                                 "TemporalRatingGraph")
        super().__init__(graph=graph)
        if bribes is not None:
            for _, bribe in bribes.items():
                for _, value in bribe.items():
                    if value < 0:
                        raise BribeMustBeGreaterThanZeroException()
        self._bribes: Dict[int, Dict[int, float]] = bribes or {}

    @classmethod
    def empty_action(cls, graph):
        return cls(graph, None)

    @classmethod
    def make_multi_action_from_single_actions(cls, actions: List[SingleBriberyAction]):
        if not actions:
            raise NoActionsToFormMultiActionException()
        graph = actions[0].briber.get_graph()
        if not all(b.briber.get_graph() is graph for b in actions):
            raise BriberyActionsOnDifferentGraphsException()
        time_step = actions[0].get_time_step()
        if not all(b.get_time_step() == time_step for b in actions):
            raise BriberyActionsAtDifferentTimesException()
        return cls(graph=graph, bribes={b.briber.get_briber_id(): b.get_bribes() for b in actions})

    def add_bribe(self, briber_id: int, node_id: int, bribe: float):
        if bribe <= 0:
            raise BribeMustBeGreaterThanZeroException()
        if node_id not in self.graph.get_customers():
            raise NodeDoesNotExistException()
        if briber_id not in range(len(self.graph.get_bribers())):
            raise BriberDoesNotExistException()
        if briber_id in self._bribes:
            if node_id in self._bribes[briber_id]:
                print("WARNING: node bribed twice in single time step, combining...", file=sys.stderr)
                self._bribes[briber_id][node_id] += bribe
            else:
                self._bribes[briber_id][node_id] = bribe
        else:
            self._bribes[briber_id] = {node_id: bribe}

    def _perform_action(self):
        bribers = self.graph.get_bribers()
        for briber_id, bribe in self._bribes.items():
            total_bribe_quantity = sum(bribe.values())
            if total_bribe_quantity > bribers[briber_id].get_resources():
                message = f"MultiBriberyAction exceeded resources available to briber {briber_id}: " \
                          f"{str(bribers[briber_id])} - {total_bribe_quantity} > {bribers[briber_id].get_resources()}"
                raise BriberyActionExceedsAvailableUtilityException(message)
        for briber_id, bribe in self._bribes.items():
            for customer, value in bribe.items():
                bribers[briber_id].bribe(node_id=customer, amount=value)

    def is_bribed(self, node_id):
        bribers = []
        for briber_id in self._bribes:
            if node_id in self._bribes[briber_id]:
                bribers.append(briber_id)
        if not bribers:
            return False, bribers
        return True, bribers

    def get_bribes(self):
        return self._bribes
